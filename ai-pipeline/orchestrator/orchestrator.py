# orchestrator.py
# AI 代码流水线编排器主程序
import argparse
import json
import os
import re
import tempfile
from typing import List, Tuple, Optional, Dict
from llm_client import LLMClient
from utils import (
    write_files_from_codeblock,
    commit_and_push,
    init_git_repo,
    validate_json_response,
    save_intermediate_result
)


def load_prompt(path: str) -> str:
    """加载提示词模板"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'提示词文件不存在: {path}')


def parse_code_blocks(llm_response: str) -> List[Tuple[str, str]]:
    """
    解析 LLM 响应中的代码块

    Args:
        llm_response: LLM 返回的原始响应

    Returns:
        代码块列表 [(路径, 内容), ...]
    """
    blocks = []

    # 匹配包含路径注释的代码块
    # 支持多种格式: # path: ..., // path: ..., <!-- path: ... -->
    pattern = re.compile(
        r'```(?:[a-zA-Z0-9]*)\n(?:#|//|<!--)\s*path:\s*(.+?)(?:-->)?\n([\s\S]*?)```',
        re.MULTILINE
    )

    for match in pattern.finditer(llm_response):
        path = match.group(1).strip()
        content = match.group(2).strip()
        blocks.append((path, content))
        print(f'  发现代码块: {path} ({len(content)} 字符)')

    if not blocks:
        print('⚠️  未找到带路径标记的代码块')

    return blocks


def generate_srs(client: LLMClient, requirement: str, output_dir: str) -> Dict:
    """
    第一步: 使用 Codex 生成 SRS

    Args:
        client: LLM 客户端
        requirement: 用户需求描述
        output_dir: 输出目录

    Returns:
        包含 srs 和 tasks 的字典
    """
    print('\n' + '='*60)
    print('步骤 1/5: 生成软件需求规格说明 (SRS)')
    print('='*60)

    prompt_path = 'orchestrator/prompts/codex_srs_prompt.txt'
    prompt = load_prompt(prompt_path).replace('{{REQUIREMENT}}', requirement)

    print('正在调用 Codex 生成 SRS...')
    srs_response = client.call_with_retry(client.call_codex, prompt, max_tokens=2000)

    # 解析响应
    srs_json = validate_json_response(srs_response)

    if srs_json and 'srs' in srs_json:
        srs_markdown = srs_json.get('srs', '')
        tasks = srs_json.get('tasks', [])
        print(f'✓ SRS 生成成功 ({len(srs_markdown)} 字符)')
        print(f'✓ 识别到 {len(tasks)} 个开发任务')
    else:
        # 降级处理: 整个响应作为 SRS
        print('⚠️  响应不是标准 JSON,将整个响应作为 SRS')
        srs_markdown = srs_response
        tasks = []

    result = {
        'srs': srs_markdown,
        'tasks': tasks,
        'raw_response': srs_response
    }

    save_intermediate_result(result, 'step1_srs', output_dir)
    return result


def generate_code(client: LLMClient, srs_data: Dict, output_dir: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    第二步: 使用 Claude 生成代码

    Args:
        client: LLM 客户端
        srs_data: SRS 数据
        output_dir: 输出目录

    Returns:
        (原始响应, 代码块列表)
    """
    print('\n' + '='*60)
    print('步骤 2/5: 生成代码实现')
    print('='*60)

    prompt_path = 'orchestrator/prompts/claude_code_prompt.txt'
    prompt = load_prompt(prompt_path)
    prompt = prompt.replace('{{SRS}}', srs_data['srs'])
    prompt = prompt.replace('{{TASKS}}', json.dumps(srs_data['tasks'], ensure_ascii=False, indent=2))

    print('正在调用 Claude 生成代码...')
    code_response = client.call_with_retry(client.call_claude, prompt, max_tokens=4000)

    # 解析代码块
    code_blocks = parse_code_blocks(code_response)

    if code_blocks:
        print(f'✓ 代码生成成功,共 {len(code_blocks)} 个文件')
    else:
        print('⚠️  未能解析出代码块')

    save_intermediate_result({
        'code_blocks': [{'path': p, 'content': c} for p, c in code_blocks],
        'raw_response': code_response
    }, 'step2_code', output_dir)

    return code_response, code_blocks


def review_and_test(client: LLMClient, srs_data: Dict, code_response: str, output_dir: str) -> Dict:
    """
    第三步: 使用 Codex 进行代码审查和测试

    Args:
        client: LLM 客户端
        srs_data: SRS 数据
        code_response: 代码生成的原始响应
        output_dir: 输出目录

    Returns:
        审查结果字典
    """
    print('\n' + '='*60)
    print('步骤 3/5: 代码审查与测试')
    print('='*60)

    prompt_path = 'orchestrator/prompts/codex_review_prompt.txt'
    prompt = load_prompt(prompt_path)
    prompt = prompt.replace('{{SRS}}', srs_data['srs'])
    prompt = prompt.replace('{{CODE_BUNDLE}}', code_response)

    print('正在调用 Codex 进行代码审查...')
    review_response = client.call_with_retry(client.call_codex, prompt, max_tokens=2000)

    # 解析审查结果
    review_json = validate_json_response(review_response)

    if review_json:
        passed = review_json.get('passed', False)
        results = review_json.get('results', [])
        defects = review_json.get('defects', [])
        tests = review_json.get('tests', {})

        print(f'审查结果: {"✓ 通过" if passed else "✗ 未通过"}')
        if defects:
            print(f'发现 {len(defects)} 个缺陷:')
            for i, defect in enumerate(defects, 1):
                print(f'  {i}. {defect}')
    else:
        print('⚠️  无法解析审查结果为 JSON')
        review_json = {
            'passed': False,
            'results': [review_response],
            'defects': ['无法解析审查结果,请查看原始响应'],
            'tests': {}
        }

    save_intermediate_result(review_json, 'step3_review', output_dir)
    return review_json


def fix_defects(client: LLMClient, defects: List[str], code_blocks: List[Tuple[str, str]], output_dir: str) -> List[Tuple[str, str]]:
    """
    第四步: 使用 Claude 修复缺陷

    Args:
        client: LLM 客户端
        defects: 缺陷列表
        code_blocks: 原始代码块
        output_dir: 输出目录

    Returns:
        修复后的代码块
    """
    print('\n' + '='*60)
    print('步骤 4/5: 修复代码缺陷')
    print('='*60)

    # 构建修复提示词
    code_bundle = '\n\n'.join([
        f'```\n# path: {path}\n{content}\n```'
        for path, content in code_blocks
    ])

    fix_prompt = f"""请修复以下代码中的缺陷:

缺陷列表:
{json.dumps(defects, ensure_ascii=False, indent=2)}

当前代码:
{code_bundle}

请返回修复后的完整代码,保持原有的 path 标记格式。
"""

    print('正在调用 Claude 修复缺陷...')
    fix_response = client.call_with_retry(client.call_claude, fix_prompt, max_tokens=4000)

    # 解析修复后的代码
    fixed_blocks = parse_code_blocks(fix_response)

    if fixed_blocks:
        print(f'✓ 代码修复完成,共 {len(fixed_blocks)} 个文件')
    else:
        print('⚠️  未能解析出修复后的代码块,使用原始代码')
        fixed_blocks = code_blocks

    save_intermediate_result({
        'fixed_blocks': [{'path': p, 'content': c} for p, c in fixed_blocks],
        'raw_response': fix_response
    }, 'step4_fix', output_dir)

    return fixed_blocks


def main(requirement: str, max_fix_iterations: int = 2):
    """
    主流程编排

    Args:
        requirement: 用户需求描述
        max_fix_iterations: 最大修复迭代次数
    """
    print('\n' + '='*60)
    print('AI 自动化代码流水线启动')
    print('='*60)
    print(f'需求: {requirement}')
    print(f'LLM Provider: {os.getenv("LLM_PROVIDER", "openai")}')

    # 初始化
    provider = os.getenv('LLM_PROVIDER', 'openai')
    client = LLMClient(provider=provider)

    # 创建输出目录
    output_dir = os.path.join(tempfile.gettempdir(), 'ai_pipeline_output')
    os.makedirs(output_dir, exist_ok=True)
    print(f'输出目录: {output_dir}')

    try:
        # 步骤 1: 生成 SRS
        srs_data = generate_srs(client, requirement, output_dir)

        # 步骤 2: 生成代码
        code_response, code_blocks = generate_code(client, srs_data, output_dir)

        if not code_blocks:
            print('\n✗ 流水线失败: 未生成任何代码')
            return

        # 写入文件
        print('\n正在将代码写入文件系统...')
        code_dir = os.path.join(output_dir, 'generated_code')
        created_files = write_files_from_codeblock(code_blocks, code_dir)
        print(f'✓ 已创建 {len(created_files)} 个文件')

        # 步骤 3: 审查和测试
        review_result = review_and_test(client, srs_data, code_response, output_dir)

        # 步骤 4 & 5: 修复循环
        iteration = 0
        while not review_result.get('passed') and iteration < max_fix_iterations:
            iteration += 1
            print(f'\n修复迭代 {iteration}/{max_fix_iterations}')

            defects = review_result.get('defects', [])
            if not defects:
                print('没有具体的缺陷信息,停止修复')
                break

            # 修复代码
            code_blocks = fix_defects(client, defects, code_blocks, output_dir)

            # 更新文件
            code_dir_fixed = os.path.join(output_dir, f'generated_code_fixed_{iteration}')
            created_files = write_files_from_codeblock(code_blocks, code_dir_fixed)

            # 重新审查
            code_response_fixed = '\n\n'.join([
                f'```\n# path: {path}\n{content}\n```'
                for path, content in code_blocks
            ])
            review_result = review_and_test(client, srs_data, code_response_fixed, output_dir)

        # 最终决策
        print('\n' + '='*60)
        print('步骤 5/5: 最终决策')
        print('='*60)

        if review_result.get('passed'):
            print('✓ 代码通过审查!')

            # 可选: 提交到 Git
            if os.getenv('AUTO_GIT_COMMIT', 'false').lower() == 'true':
                print('\n正在提交到 Git...')
                final_code_dir = os.path.join(output_dir, f'generated_code_fixed_{iteration}' if iteration > 0 else 'generated_code')

                if init_git_repo(final_code_dir):
                    success = commit_and_push(
                        final_code_dir,
                        'ai-generated',
                        f'AI generated code - {requirement[:50]}',
                        create_branch=True
                    )
                    if success:
                        print('✓ 代码已提交到分支 ai-generated')
                    else:
                        print('⚠️  提交失败,请手动操作')
            else:
                print('\n提示: 设置环境变量 AUTO_GIT_COMMIT=true 可自动提交代码')
        else:
            print('✗ 代码审查未通过')
            print('缺陷列表:')
            for i, defect in enumerate(review_result.get('defects', []), 1):
                print(f'  {i}. {defect}')
            print('\n建议: 检查输出目录中的中间结果,手动修复问题')

        print(f'\n所有输出已保存至: {output_dir}')

    except Exception as e:
        print(f'\n✗ 流水线执行失败: {str(e)}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AI 自动化代码流水线 - 从需求到可运行代码'
    )
    parser.add_argument(
        '--requirement',
        required=True,
        help='用户需求描述'
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=2,
        help='最大修复迭代次数 (默认: 2)'
    )

    args = parser.parse_args()
    main(args.requirement, args.max_iterations)

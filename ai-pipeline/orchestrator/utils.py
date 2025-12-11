# utils.py
# 工具函数:文件操作、Git 操作等
import json
import os
import tempfile
from typing import List, Tuple, Optional


def write_files_from_codeblock(codeblocks: List[Tuple[str, str]], base_dir: str) -> List[str]:
    """
    将代码块写入文件系统

    Args:
        codeblocks: 代码块列表,每个元素为 (相对路径, 文件内容) 元组
        base_dir: 基础目录

    Returns:
        创建的文件路径列表
    """
    created_files = []

    for path, content in codeblocks:
        # 安全性检查:防止路径遍历攻击
        if '..' in path or path.startswith('/'):
            print(f'警告:跳过不安全的路径: {path}')
            continue

        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(full_path)
            print(f'✓ 已创建: {path}')
        except Exception as e:
            print(f'✗ 创建失败 {path}: {str(e)}')

    return created_files


def commit_and_push(
    repo_dir: str,
    branch_name: str,
    commit_message: str,
    remote: str = 'origin',
    create_branch: bool = True
) -> bool:
    """
    提交代码并推送到远程仓库

    Args:
        repo_dir: 仓库目录
        branch_name: 分支名称
        commit_message: 提交信息
        remote: 远程仓库名称
        create_branch: 是否创建新分支

    Returns:
        是否成功
    """
    try:
        from git import Repo, GitCommandError

        repo = Repo(repo_dir)

        # 检查是否有未提交的更改
        if not repo.is_dirty() and not repo.untracked_files:
            print('没有需要提交的更改')
            return False

        # 创建或切换分支
        if create_branch:
            try:
                repo.git.checkout('-b', branch_name)
                print(f'✓ 已创建分支: {branch_name}')
            except GitCommandError:
                repo.git.checkout(branch_name)
                print(f'✓ 已切换到分支: {branch_name}')
        else:
            repo.git.checkout(branch_name)

        # 添加所有文件
        repo.git.add(all=True)

        # 提交
        repo.index.commit(commit_message)
        print(f'✓ 已提交: {commit_message}')

        # 推送到远程
        try:
            origin = repo.remote(remote)
            origin.push(branch_name)
            print(f'✓ 已推送到 {remote}/{branch_name}')
            return True
        except GitCommandError as e:
            print(f'✗ 推送失败: {str(e)}')
            print('提示:请确保已配置 Git 凭据和远程仓库')
            return False

    except Exception as e:
        print(f'✗ Git 操作失败: {str(e)}')
        return False


def init_git_repo(repo_dir: str, remote_url: Optional[str] = None) -> bool:
    """
    初始化 Git 仓库

    Args:
        repo_dir: 仓库目录
        remote_url: 远程仓库 URL (可选)

    Returns:
        是否成功
    """
    try:
        from git import Repo

        # 初始化仓库
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            repo = Repo.init(repo_dir)
            print(f'✓ 已初始化 Git 仓库: {repo_dir}')
        else:
            repo = Repo(repo_dir)
            print(f'✓ Git 仓库已存在: {repo_dir}')

        # 添加远程仓库
        if remote_url:
            try:
                repo.create_remote('origin', remote_url)
                print(f'✓ 已添加远程仓库: {remote_url}')
            except Exception:
                print(f'远程仓库 origin 已存在')

        return True

    except Exception as e:
        print(f'✗ 初始化仓库失败: {str(e)}')
        return False


def validate_json_response(response: str) -> Optional[dict]:
    """
    验证并解析 JSON 响应

    Args:
        response: LLM 返回的原始响应

    Returns:
        解析后的 JSON 对象,如果失败则返回 None
    """
    try:
        # 尝试直接解析
        return json.loads(response)
    except json.JSONDecodeError:
        # 尝试提取 JSON 代码块
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试提取 { ... } 内容
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

    return None


def save_intermediate_result(data: dict, step: str, output_dir: str) -> str:
    """
    保存中间结果

    Args:
        data: 要保存的数据
        step: 步骤名称
        output_dir: 输出目录

    Returns:
        保存的文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f'{step}.json')

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'✓ 已保存中间结果: {filepath}')
        return filepath
    except Exception as e:
        print(f'✗ 保存失败: {str(e)}')
        return ''

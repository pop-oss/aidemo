# llm_client_v2.py
# LLM 客户端封装,支持 OpenAI、Anthropic Claude 和第三方 API
import os
import json
from typing import Optional


class LLMClient:
    """统一的 LLM 客户端接口,支持第三方 API"""

    def __init__(self, provider: str = 'openai'):
        """
        初始化 LLM 客户端

        Args:
            provider: LLM 提供商 ('openai' 或 'anthropic')
        """
        self.provider = provider.lower()
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.claude_key = os.getenv('CLAUDE_API_KEY')

        # 支持第三方 API 和自定义配置
        self.openai_base_url = os.getenv('OPENAI_API_BASE')  # 第三方 API 端点
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')  # 自定义模型

        # 调试模式
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'

        if self.provider == 'openai' and not self.openai_key:
            raise ValueError('需要设置 OPENAI_API_KEY 环境变量')
        if self.provider == 'anthropic' and not self.claude_key:
            raise ValueError('需要设置 CLAUDE_API_KEY 环境变量')

        if self.debug:
            print(f'[DEBUG] LLM Provider: {self.provider}')
            print(f'[DEBUG] API Base URL: {self.openai_base_url or "默认"}')
            print(f'[DEBUG] Model: {self.openai_model}')

    def call_codex(self, prompt: str, max_tokens: int = 1500) -> str:
        """
        调用 Codex 模型 (用于 SRS 生成和代码审查)

        Args:
            prompt: 输入提示词
            max_tokens: 最大生成 token 数

        Returns:
            模型生成的文本
        """
        if self.provider == 'openai':
            try:
                import openai

                # 创建客户端,支持自定义 base_url
                client_kwargs = {'api_key': self.openai_key}
                if self.openai_base_url:
                    client_kwargs['base_url'] = self.openai_base_url
                    if self.debug:
                        print(f'[DEBUG] 使用第三方 API: {self.openai_base_url}')

                client = openai.OpenAI(**client_kwargs)

                response = client.chat.completions.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的软件工程师和需求分析师。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                return response.choices[0].message.content
            except Exception as e:
                raise RuntimeError(f'OpenAI API 调用失败: {str(e)}')
        else:
            raise NotImplementedError(f'Provider {self.provider} 不支持 Codex 调用')

    def call_claude(self, prompt: str, max_tokens: int = 4000) -> str:
        """
        调用 Claude 模型 (用于代码生成和修复)

        Args:
            prompt: 输入提示词
            max_tokens: 最大生成 token 数

        Returns:
            模型生成的文本
        """
        if self.provider == 'anthropic':
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=self.claude_key)

                response = client.messages.create(
                    model='claude-3-5-sonnet-20241022',
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
                return response.content[0].text
            except Exception as e:
                raise RuntimeError(f'Claude API 调用失败: {str(e)}')
        elif self.provider == 'openai':
            # 使用 OpenAI 作为 Claude 的替代
            try:
                import openai

                # 创建客户端,支持自定义 base_url
                client_kwargs = {'api_key': self.openai_key}
                if self.openai_base_url:
                    client_kwargs['base_url'] = self.openai_base_url

                client = openai.OpenAI(**client_kwargs)

                response = client.chat.completions.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": "你是一个资深软件工程师,擅长编写高质量、可维护的代码。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                return response.choices[0].message.content
            except Exception as e:
                raise RuntimeError(f'OpenAI API 调用失败: {str(e)}')
        else:
            raise NotImplementedError(f'Provider {self.provider} 不支持 Claude 调用')

    def call_with_retry(self, func, *args, max_retries: int = 3, **kwargs) -> str:
        """
        带重试机制的 API 调用

        Args:
            func: 要调用的函数
            max_retries: 最大重试次数
            *args, **kwargs: 传递给函数的参数

        Returns:
            函数返回值
        """
        import time

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f'API 调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}')
                time.sleep(2 ** attempt)  # 指数退避

        raise RuntimeError('API 调用重试次数耗尽')

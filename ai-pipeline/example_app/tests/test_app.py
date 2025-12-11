# path: example_app/tests/test_app.py
"""
示例微服务单元测试
"""
import pytest
import json
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from example_app.src.app import app


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """健康检查端点测试"""

    def test_health_check_returns_200(self, client):
        """测试健康检查返回 200 状态码"""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_check_returns_correct_structure(self, client):
        """测试健康检查返回正确的 JSON 结构"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'status' in data
        assert 'service' in data
        assert 'version' in data
        assert data['status'] == 'ok'


class TestAddEndpoint:
    """加法端点测试"""

    def test_add_two_positive_numbers(self, client):
        """测试两个正数相加"""
        response = client.post('/add', json={'a': 1, 'b': 2})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 3
        assert data['operation'] == 'add'

    def test_add_negative_numbers(self, client):
        """测试负数相加"""
        response = client.post('/add', json={'a': -5, 'b': 3})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == -2

    def test_add_with_floats(self, client):
        """测试浮点数相加"""
        response = client.post('/add', json={'a': 1.5, 'b': 2.5})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 4.0

    def test_add_with_invalid_input(self, client):
        """测试无效输入"""
        response = client.post('/add', json={'a': 'invalid', 'b': 2})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_with_missing_parameter(self, client):
        """测试缺少参数"""
        response = client.post('/add', json={'a': 1})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_with_empty_body(self, client):
        """测试空请求体"""
        response = client.post('/add', json={})
        assert response.status_code == 400


class TestMultiplyEndpoint:
    """乘法端点测试"""

    def test_multiply_two_positive_numbers(self, client):
        """测试两个正数相乘"""
        response = client.post('/multiply', json={'a': 3, 'b': 4})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 12
        assert data['operation'] == 'multiply'

    def test_multiply_by_zero(self, client):
        """测试乘以零"""
        response = client.post('/multiply', json={'a': 5, 'b': 0})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 0

    def test_multiply_negative_numbers(self, client):
        """测试负数相乘"""
        response = client.post('/multiply', json={'a': -3, 'b': 4})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == -12


class TestDivideEndpoint:
    """除法端点测试"""

    def test_divide_two_numbers(self, client):
        """测试两数相除"""
        response = client.post('/divide', json={'a': 10, 'b': 2})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 5.0
        assert data['operation'] == 'divide'

    def test_divide_by_zero(self, client):
        """测试除以零"""
        response = client.post('/divide', json={'a': 10, 'b': 0})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Division by zero' in data['details']

    def test_divide_negative_numbers(self, client):
        """测试负数相除"""
        response = client.post('/divide', json={'a': -10, 'b': 2})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == -5.0


class TestErrorHandling:
    """错误处理测试"""

    def test_404_error(self, client):
        """测试 404 错误"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_405_method_not_allowed(self, client):
        """测试 405 方法不允许错误"""
        response = client.get('/add')
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

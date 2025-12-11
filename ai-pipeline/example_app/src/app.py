# path: example_app/src/app.py
"""
示例 Flask 微服务
提供简单的计算和健康检查 API
"""
from flask import Flask, jsonify, request
from functools import wraps
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def error_handler(func):
    """统一错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f'ValueError in {func.__name__}: {str(e)}')
            return jsonify({'error': 'Invalid input', 'details': str(e)}), 400
        except Exception as e:
            logger.error(f'Unexpected error in {func.__name__}: {str(e)}')
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper


@app.route('/health')
def health():
    """健康检查端点"""
    logger.info('Health check requested')
    return jsonify({
        'status': 'ok',
        'service': 'example_app',
        'version': '1.0.0'
    })


@app.route('/add', methods=['POST'])
@error_handler
def add():
    """
    加法运算端点

    请求体示例:
    {
        "a": 1,
        "b": 2
    }

    返回示例:
    {
        "result": 3,
        "operation": "add"
    }
    """
    data = request.json or {}

    a = data.get('a')
    b = data.get('b')

    # 参数验证
    if a is None or b is None:
        raise ValueError('Missing required parameters: a and b')

    # 类型转换
    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        raise ValueError('Parameters a and b must be numeric')

    result = a + b
    logger.info(f'Addition: {a} + {b} = {result}')

    return jsonify({
        'result': result,
        'operation': 'add'
    })


@app.route('/multiply', methods=['POST'])
@error_handler
def multiply():
    """
    乘法运算端点

    请求体示例:
    {
        "a": 3,
        "b": 4
    }

    返回示例:
    {
        "result": 12,
        "operation": "multiply"
    }
    """
    data = request.json or {}

    a = data.get('a')
    b = data.get('b')

    if a is None or b is None:
        raise ValueError('Missing required parameters: a and b')

    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        raise ValueError('Parameters a and b must be numeric')

    result = a * b
    logger.info(f'Multiplication: {a} * {b} = {result}')

    return jsonify({
        'result': result,
        'operation': 'multiply'
    })


@app.route('/divide', methods=['POST'])
@error_handler
def divide():
    """
    除法运算端点

    请求体示例:
    {
        "a": 10,
        "b": 2
    }

    返回示例:
    {
        "result": 5.0,
        "operation": "divide"
    }
    """
    data = request.json or {}

    a = data.get('a')
    b = data.get('b')

    if a is None or b is None:
        raise ValueError('Missing required parameters: a and b')

    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        raise ValueError('Parameters a and b must be numeric')

    if b == 0:
        raise ValueError('Division by zero is not allowed')

    result = a / b
    logger.info(f'Division: {a} / {b} = {result}')

    return jsonify({
        'result': result,
        'operation': 'divide'
    })


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on the server'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """405 错误处理"""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The method is not allowed for the requested URL'
    }), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

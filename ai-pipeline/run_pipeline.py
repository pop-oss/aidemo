#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import io

# Windows UTF-8 fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Check API key
if not os.getenv('OPENAI_API_KEY'):
    print('[ERROR] OPENAI_API_KEY not set')
    print('Please configure .env file')
    sys.exit(1)

# Show config in debug mode
if os.getenv('DEBUG', '').lower() == 'true':
    print('[DEBUG] Config loaded:')
    print(f'  Provider: {os.getenv("LLM_PROVIDER", "openai")}')
    print(f'  API Base: {os.getenv("OPENAI_API_BASE", "default")}')
    print(f'  Model: {os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")}')
    print()

# Run orchestrator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))
from orchestrator import main
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--requirement', required=True)
parser.add_argument('--max-iterations', type=int, default=2)
args = parser.parse_args()

main(args.requirement, args.max_iterations)

import subprocess
from langchain_core.tools import tool

@tool
def execute_script(code: str) -> str:
    """
    提供されたPythonコードを実行し、その結果を返します。

    Args:
        code (str): 実行するPythonコード。

    Returns:
        str: スクリプトの実行結果。
    """
    filename = 'temp_script.py'
    with open(filename, 'w') as file:
        file.write(code)
    
    result = subprocess.run(['python', filename], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr
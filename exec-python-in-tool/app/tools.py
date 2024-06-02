import subprocess
from datetime import datetime
import os
from langchain_core.tools import tool

TOOL_ROOT_FOLDER = "temps"
if not os.path.exists(TOOL_ROOT_FOLDER):
    os.makedirs(TOOL_ROOT_FOLDER)


@tool
def get_now():
    """
    現在の日時を取得します。

    Returns:
        datetime: 現在の日時。
    """
    return datetime.now()

@tool
def create_and_edit_file(filename: str, source_code: str) -> str:
    """
    指定されたファイル名でソースコードを含むファイルを作成し、そのファイル名を返します。

    Args:
        filename (str): 作成するファイルの名前。
        source_code (str): ファイルに書き込むソースコード。

    Returns:
        str: 作成されたファイルの完全なパス。
    """
    full_path = os.path.join(TOOL_ROOT_FOLDER, filename)
    with open(full_path, 'w') as file:
        file.write(source_code)
    
    return filename

@tool
def list_files() -> list:
    """
    TOOL_ROOT_FOLDER内のファイル一覧を取得します。

    Returns:
        list: ファイル名のリスト。
    """
    return os.listdir(TOOL_ROOT_FOLDER)
    

@tool
def execute_python_file(filename: str) -> str:
    """
    指定されたファイル名のPythonファイルを実行し、その結果を返します。

    Args:
        filename (str): 実行するファイルの名前。

    Returns:
        str: スクリプトの実行結果。
    """
    full_path = os.path.join(TOOL_ROOT_FOLDER, filename)
    
    result = subprocess.run(['python', full_path], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

@tool
def poetry_command(command: list[str], folder: str = "temps") -> str:
    """
    Poetryコマンドを実行し、その結果を返します。コマンドは指定されたフォルダ内で実行されます。

    Args:
        command (list[str]): 実行するPoetryコマンドのリスト。
        folder (str): コマンドを実行するフォルダ。

    Returns:
        str: コマンドの実行結果。
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    result = subprocess.run(['poetry'] + command, capture_output=True, text=True)
    os.chdir('..')
    return result.stdout if result.returncode == 0 else result.stderr

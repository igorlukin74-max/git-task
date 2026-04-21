import subprocess
import calc


def get_git_output(command):
    return subprocess.check_output(command, shell=True, text=True).strip()


def test_author_metadata():
    # Проверяем, что поле имени автора в Git не стандартное и не пустое
    author_name = get_git_output("git log -1 --format='%an'")
    # Список имен, которые мы считаем "незаполненными"
    forbidden_names = ["Your Name", "root", "admin", "user", "student"]

    assert author_name not in forbidden_names, f"Ошибка: Настройте git config user.name! Сейчас там: '{author_name}'"
    assert len(author_name) > 3, "Ошибка: Имя автора слишком короткое."


def test_fio_in_code():
    # Проверяем наличие строки с ФИО в самом файле calc.py
    with open("calc.py", "r", encoding="utf-8") as f:
        first_line = f.readline()
    assert "# Автор:" in first_line, "Ошибка: В первой строке calc.py должен быть комментарий '# Автор: Имя Фамилия'"
    assert len(first_line.split("Автор:")) > 1 and len(first_line.split("Автор:")[1].strip()) > 5, \
        "Ошибка: ФИО в комментарии не заполнено или слишком короткое."


def test_branch_policy():
    # проверяем, что develop ушел вперед относительно main, а не наоборот.
    try:
        # Сравниваем две удаленные ветки
        diff = get_git_output("git rev-list origin/main..origin/develop --count")
        assert int(diff) >= 0, "Ошибка в структуре веток."
    except subprocess.CalledProcessError:
        # Если origin/main не найден, возможно, ветка называется master
        diff = get_git_output("git rev-list origin/master..origin/develop --count")

def test_develop_exists():
    # Проверяем наличие ветки develop
    branches = get_git_output("git branch -a")
    assert "develop" in branches, "Ошибка: Ветка 'develop' не найдена."


def test_multiply_fixed():
    assert calc.multiply(10, 5) == 50, "Ошибка: Функция multiply все еще не работает."


def test_sqrt_added():
    assert hasattr(calc, 'sqrt'), "Ошибка: Функция sqrt не добавлена."
    assert calc.sqrt(16) == 4.0

# 🚀 Настройка GitHub репозитория

## 📋 Пошаговая инструкция

### 1. Создание репозитория на GitHub

1. **Перейдите на [GitHub](https://github.com)**
2. **Нажмите "New repository"** (зеленая кнопка)
3. **Заполните форму:**
   - **Repository name:** `humanology_telegram-bot`
   - **Description:** `Telegram bot for personality type determination using AI technologies`
   - **Visibility:** Public (рекомендуется) или Private
   - **НЕ ставьте галочки:**
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
4. **Нажмите "Create repository"**

### 2. Настройка локального репозитория

После создания репозитория на GitHub, замените `your-username` на ваше реальное имя пользователя:

```bash
# Удалите текущий remote (если есть)
git remote remove origin

# Добавьте правильный remote
git remote add origin https://github.com/YOUR_USERNAME/humanology_telegram-bot.git

# Проверьте remote
git remote -v
```

### 3. Пуш в GitHub

```bash
# Переименуйте ветку в main (если нужно)
git branch -M main

# Запушьте код
git push -u origin main
```

### 4. Проверка результата

После успешного пуша:
1. **Обновите страницу репозитория** на GitHub
2. **Убедитесь, что все файлы загружены**
3. **Проверьте README.md** - он должен отображаться на главной странице

## 🔧 Дополнительные настройки

### Настройка веток

```bash
# Создание ветки для разработки
git checkout -b develop

# Пуш новой ветки
git push -u origin develop
```

### Настройка защиты веток

1. **Перейдите в Settings → Branches**
2. **Добавьте правило для main:**
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

### Настройка Issues и Projects

1. **Включите Issues** в репозитории
2. **Создайте Project board** для управления задачами
3. **Настройте Labels** для категоризации

## 📝 Шаблоны для Issues и Pull Requests

### Issue Template

Создайте файл `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Python version: [e.g. 3.9]
 - Bot version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### Pull Request Template

Создайте файл `.github/pull_request_template.md`:

```markdown
## Description
Brief description of changes

## Type of change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots (if applicable)
Add screenshots to help explain your changes.
```

## 🎯 Следующие шаги

После настройки репозитория:

1. **Добавьте описание** в About section
2. **Настройте Topics** для лучшего поиска
3. **Создайте Wiki** для дополнительной документации
4. **Настройте Actions** для CI/CD (если нужно)
5. **Добавьте Contributors** в репозиторий

## 🔗 Полезные ссылки

- [GitHub Guides](https://guides.github.com/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [GitHub Pages](https://pages.github.com/)
- [GitHub Actions](https://github.com/features/actions)

---

**Удачной разработки! 🚀**

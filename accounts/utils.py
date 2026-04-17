def get_user_role(user):
    """Возвращает роль пользователя: guest / client / manager / admin"""
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='Менеджеры').exists():
        return 'manager'
    if user.groups.filter(name='Клиенты').exists():
        return 'client'
    # Аутентифицированный пользователь без группы считается клиентом
    return 'client'

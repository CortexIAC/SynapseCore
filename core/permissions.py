def is_admin(state):
    return getattr(state, "role", "") == "overseer"
from app.core.casbin import get_enforcer

TENANT_ID = "1"


def seed_policies():
    e = get_enforcer()
    e.clear_policy()
    e.add_policy("admin", "*", "*", "read", "allow")
    e.add_policy("manager", "*", "*", "read", "allow")
    e.add_policy("support", "*", "*", "read", "allow")
    e.add_policy("guest", "*", "*", "read", "allow")
    e.save_policy()


def seed_roles_for_tenant_1():
    e = get_enforcer()
    if not e.get_policy():
        seed_policies()
    e.add_role_for_user_in_domain("1", "admin", TENANT_ID)
    e.add_role_for_user_in_domain("2", "manager", TENANT_ID)
    e.add_role_for_user_in_domain("3", "support", TENANT_ID)
    e.add_role_for_user_in_domain("4", "guest", TENANT_ID)
    e.save_policy()


def seed_all():
    seed_policies()
    seed_roles_for_tenant_1()


if __name__ == "__main__":
    seed_all()
from app.core.casbin import get_casbin_enforcer


def main():
    e = get_casbin_enforcer()

    e.clear_policy()

    # Tenant 1: alice is admin
    e.add_policy("admin", "1", "admin_panel", "read")
    e.add_policy("admin", "1", "admin_panel", "write")
    e.add_policy("admin", "1", "users", "read")
    e.add_policy("admin", "1", "users", "write")
    e.add_grouping_policy("alice", "admin", "1")

    # Tenant 2: bob is regular user who can read data1
    e.add_policy("user", "2", "data1", "read")
    e.add_grouping_policy("bob", "user", "2")

    e.save_policy()


if __name__ == "__main__":
    main()
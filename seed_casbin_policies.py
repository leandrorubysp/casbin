from app.core.casbin import get_casbin_enforcer


def main():
    e = get_casbin_enforcer()

    e.clear_policy()

    e.add_policy("admin", "admin_panel", "read")
    e.add_policy("admin", "admin_panel", "write")
    e.add_policy("admin", "users", "read")
    e.add_policy("admin", "users", "write")

    e.add_grouping_policy("alice", "admin")

    e.add_policy("user", "data1", "read")
    e.add_grouping_policy("bob", "user")

    e.save_policy()


if __name__ == "__main__":
    main()
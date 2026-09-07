interface Prototype<T> {
  clone(): T;
}

class UserProfile implements Prototype<UserProfile> {
  constructor(
    public name: string,
    public permissions: string[],
  ) {}

  clone(): UserProfile {
    return new UserProfile(this.name, [...this.permissions]);
  }
}

const prototype = new UserProfile("Admin", ["read", "write", "delete"]);

const user = prototype.clone();

user.name = "Manager";

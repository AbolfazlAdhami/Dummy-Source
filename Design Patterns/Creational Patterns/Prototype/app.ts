interface Prototype<T> {
  clone(): T;
}

class Shape implements Prototype<Shape> {
  constructor(public color: string) {}

  clone(): Shape {
    return new Shape(this.color);
  }
}

const circle1 = new Shape("Red");
const circle2 = circle1.clone();
console.log(circle1.color); // Output: Red
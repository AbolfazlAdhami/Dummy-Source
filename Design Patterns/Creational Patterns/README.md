# Creational Design Patterns in TypeScript

A practical guide to the **5 classic GoF Creational Design Patterns**:

1. Singleton
2. Factory Method
3. Abstract Factory
4. Builder
5. Prototype

The goal of this README is not only to explain each pattern, but to show **when to use it, how it relates to OOP and SOLID, how many classes it typically introduces, and how the patterns relate to each other**.

---

## Table of Contents

- [What Are Creational Patterns?](#what-are-creational-patterns)
- [Quick Comparison](#quick-comparison)
- [1. Singleton](#1-singleton)
- [2. Factory Method](#2-factory-method)
- [3. Abstract Factory](#3-abstract-factory)
- [4. Builder](#4-builder)
- [5. Prototype](#5-prototype)
- [Factory Method vs Abstract Factory](#factory-method-vs-abstract-factory)
- [Builder vs Factory](#builder-vs-factory)
- [Prototype vs Builder](#prototype-vs-builder)
- [How They Relate to OOP](#how-they-relate-to-oop)
- [How They Relate to SOLID](#how-they-relate-to-solid)
- [How the Patterns Can Work Together](#how-the-patterns-can-work-together)
- [Choosing the Right Pattern](#choosing-the-right-pattern)
- [Class Count and Complexity](#class-count-and-complexity)
- [Real-World Example](#real-world-example)
- [Final Cheat Sheet](#final-cheat-sheet)

---

# What Are Creational Patterns?

Creational Design Patterns deal with **object creation**.

Instead of tightly coupling application code to concrete classes:

```ts
const payment = new StripePayment();
```

we can introduce an abstraction:

```ts
const payment = factory.createPayment();
```

This gives us more control over:

- Which object is created
- How objects are constructed
- Which implementation is used
- Whether objects are copied or newly created
- Whether multiple objects belong to the same product family
- How object creation is separated from business logic

The five classic GoF Creational Patterns are:

```text
Creational Patterns
│
├── Singleton
├── Factory Method
├── Abstract Factory
├── Builder
└── Prototype
```

---

# Quick Comparison

| Pattern          | Main Question                                     | Typical Result               |
| ---------------- | ------------------------------------------------- | ---------------------------- |
| Singleton        | Should there be only one instance?                | One shared instance          |
| Factory Method   | Which implementation should I create?             | One product                  |
| Abstract Factory | Which family of related products should I create? | Multiple compatible products |
| Builder          | How should I construct this complex object?       | One complex object           |
| Prototype        | How can I copy this existing object?              | Clone of an existing object  |

A useful mental model:

```text
Singleton
    → instance count

Prototype
    → copying

Builder
    → construction process

Factory Method
    → product implementation

Abstract Factory
    → product family
```

---

# 1. Singleton

## Intent

Ensure that a class has **only one instance** and provide a global access point to it.

## Problem

Suppose multiple parts of your application create database managers:

```ts
const db1 = new Database();
const db2 = new Database();
const db3 = new Database();
```

If the application requires a single shared instance, this can cause unnecessary connections or inconsistent state.

## Structure

```text
Database
    │
    └── one instance
```

## TypeScript Example

```ts
class Database {
  private static instance: Database;

  private constructor() {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }

    return Database.instance;
  }
}
```

Usage:

```ts
const db1 = Database.getInstance();
const db2 = Database.getInstance();

console.log(db1 === db2); // true
```

## Typical Number of Classes

Usually:

```text
1 class
```

## OOP Concepts

Singleton mainly uses:

- Encapsulation
- Private constructor
- Static members
- Controlled object creation

## Use Cases

- Configuration manager
- Logger
- Cache manager
- Resource manager
- Application-wide state where a single instance is genuinely required

## Advantages

- Guarantees one instance
- Centralized access
- Can control resource initialization

## Disadvantages

- Can introduce global mutable state
- Can make testing harder
- Can hide dependencies
- Often overused

### Important Note for NestJS

NestJS providers are singleton-scoped by default. Therefore, manually implementing the classic Singleton pattern is often unnecessary.

Prefer:

```ts
@Injectable()
export class ConfigService {}
```

with dependency injection rather than implementing `getInstance()` yourself.

---

# 2. Factory Method

## Intent

Define an interface for creating an object, while allowing subclasses or concrete creators to decide which concrete product is created.

## Problem

Suppose you have:

```text
Notification
├── EmailNotification
├── SMSNotification
└── PushNotification
```

The client should not need to know which concrete class to instantiate.

## Product

```ts
interface Notification {
  send(): void;
}
```

## Concrete Products

```ts
class EmailNotification implements Notification {
  send(): void {
    console.log("Sending email");
  }
}

class SMSNotification implements Notification {
  send(): void {
    console.log("Sending SMS");
  }
}
```

## Creator

```ts
abstract class NotificationCreator {
  abstract createNotification(): Notification;

  notify(): void {
    const notification = this.createNotification();

    notification.send();
  }
}
```

## Concrete Creators

```ts
class EmailCreator extends NotificationCreator {
  createNotification(): Notification {
    return new EmailNotification();
  }
}

class SMSCreator extends NotificationCreator {
  createNotification(): Notification {
    return new SMSNotification();
  }
}
```

Usage:

```ts
const creator = new EmailCreator();

creator.notify();
```

## Structure

```text
Notification
│
├── EmailNotification
├── SMSNotification
└── PushNotification


NotificationCreator
│
├── EmailCreator
├── SMSCreator
└── PushCreator
```

## Typical Number of Classes

Potentially:

```text
1 Product interface
+
N Concrete Products
+
1 Creator
+
N Concrete Creators
```

## OOP Concepts

Factory Method strongly uses:

- Abstraction
- Polymorphism
- Inheritance
- Encapsulation

## SOLID

Especially related to:

- Open/Closed Principle
- Dependency Inversion Principle
- Single Responsibility Principle

## Use Cases

- Notification systems
- Payment providers
- File parsers
- Exporters
- Database drivers
- Storage providers
- Logging implementations

---

# 3. Abstract Factory

## Intent

Provide an interface for creating **families of related or compatible objects** without specifying their concrete classes.

## Problem

Suppose you are building a UI framework:

```text
Windows
├── Button
├── Checkbox
└── Input

Mac
├── Button
├── Checkbox
└── Input
```

You don't want to accidentally combine:

```text
WindowsButton
+
MacCheckbox
+
LinuxInput
```

Instead, choose one product family.

## Abstract Products

```ts
interface Button {
  render(): void;
}

interface Checkbox {
  render(): void;
}

interface Input {
  render(): void;
}
```

## Abstract Factory

```ts
interface UIFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
  createInput(): Input;
}
```

## Concrete Products

```ts
class WindowsButton implements Button {
  render(): void {
    console.log("Windows button");
  }
}

class WindowsCheckbox implements Checkbox {
  render(): void {
    console.log("Windows checkbox");
  }
}

class WindowsInput implements Input {
  render(): void {
    console.log("Windows input");
  }
}
```

## Concrete Factory

```ts
class WindowsFactory implements UIFactory {
  createButton(): Button {
    return new WindowsButton();
  }

  createCheckbox(): Checkbox {
    return new WindowsCheckbox();
  }

  createInput(): Input {
    return new WindowsInput();
  }
}
```

A Mac factory could provide:

```text
MacButton
MacCheckbox
MacInput
```

## Structure

```text
                UIFactory
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 WindowsFactory             MacFactory
        │                       │
   ┌────┼────┐             ┌────┼────┐
   ▼    ▼    ▼             ▼    ▼    ▼
 Button Input Checkbox    Button Input Checkbox
```

## Typical Number of Classes

Abstract Factory can introduce many classes:

```text
1 Abstract Factory
+
N Concrete Factories
+
M Abstract Products
+
N × M Concrete Products
```

For example:

```text
3 families
4 product types
```

can mean:

```text
3 × 4 = 12 concrete products
```

plus the factories and abstractions.

## OOP Concepts

Uses:

- Abstraction
- Polymorphism
- Composition
- Encapsulation
- Sometimes inheritance

## SOLID

Especially related to:

- Open/Closed Principle
- Dependency Inversion Principle
- Single Responsibility Principle

## Use Cases

- Cross-platform UI
- Cloud provider integrations
- Payment provider ecosystems
- Database provider families
- Theme systems
- OS-specific components

---

# 4. Builder

## Intent

Separate the construction of a complex object from its representation, allowing the object to be constructed step-by-step.

## Problem

A class with many parameters can become difficult to construct:

```ts
new HttpRequest("POST", "/users", headers, body, timeout, retry, authentication, cache);
```

It is hard to know what each argument means.

## Builder Solution

```ts
const request = new HttpRequestBuilder().setMethod("POST").setUrl("/users").addHeader("Authorization", "Bearer token").setBody({ name: "Abolfazl" }).setTimeout(5000).build();
```

## Product

```ts
class HttpRequest {
  constructor(
    public readonly method: string,
    public readonly url: string,
    public readonly headers: Record<string, string>,
    public readonly body?: unknown,
    public readonly timeout?: number,
  ) {}
}
```

## Builder

```ts
class HttpRequestBuilder {
  private method = "GET";
  private url = "";
  private headers: Record<string, string> = {};
  private body?: unknown;
  private timeout?: number;

  setMethod(method: string): this {
    this.method = method;
    return this;
  }

  setUrl(url: string): this {
    this.url = url;
    return this;
  }

  addHeader(key: string, value: string): this {
    this.headers[key] = value;
    return this;
  }

  setBody(body: unknown): this {
    this.body = body;
    return this;
  }

  setTimeout(timeout: number): this {
    this.timeout = timeout;
    return this;
  }

  build(): HttpRequest {
    if (!this.url) {
      throw new Error("URL is required");
    }

    return new HttpRequest(this.method, this.url, { ...this.headers }, this.body, this.timeout);
  }
}
```

## Fluent Interface

The following:

```ts
builder.setMethod("POST").setUrl("/users").setTimeout(5000);
```

is called a **fluent interface**.

Methods return `this`:

```ts
setUrl(url: string): this {
  this.url = url;
  return this;
}
```

## Typical Number of Classes

Modern implementation:

```text
1 Builder
+
1 Product
```

Classic GoF implementation can contain:

```text
Director
Abstract Builder
Concrete Builder
Product
```

The Director is optional in many modern TypeScript implementations.

## Use Cases

- HTTP request builders
- SQL/query builders
- Complex configuration
- Test fixtures
- Domain objects
- API clients
- Document generation

## Advantages

- Readable construction
- Handles many optional parameters
- Centralized validation
- Supports immutable final objects
- Separates construction from representation

## Disadvantages

- More code
- More abstraction
- Mutable builder state can be problematic
- Can be unnecessary for simple objects

---

# 5. Prototype

## Intent

Create new objects by **copying an existing object**, rather than constructing a new object from scratch.

## Problem

Suppose an object is expensive or complicated to construct:

```ts
const original = new Document(...many parameters...);
```

If you need a similar document, cloning may be simpler.

## Prototype Interface

```ts
interface Prototype<T> {
  clone(): T;
}
```

## Concrete Prototype

```ts
class User implements Prototype<User> {
  constructor(
    public name: string,
    public email: string,
  ) {}

  clone(): User {
    return new User(this.name, this.email);
  }
}
```

Usage:

```ts
const user1 = new User("Abolfazl", "ab@example.com");

const user2 = user1.clone();

console.log(user1 === user2); // false
```

The objects have different references but can contain equivalent data.

## Typical Number of Classes

Usually:

```text
1 Prototype interface
+
1+ Concrete Prototypes
```

## Important Concept: Shallow vs Deep Copy

Be careful when the object contains nested objects.

```ts
class User {
  constructor(public profile: Profile) {}

  clone(): User {
    return new User(this.profile);
  }
}
```

This may copy the reference to `profile`.

For complex nested structures, you may need a deep clone strategy.

## Use Cases

- Templates
- Game objects
- Complex documents
- Configuration snapshots
- Expensive object creation
- Object duplication

---

# Factory Method vs Abstract Factory

This is one of the most important distinctions.

## Factory Method

Creates a product:

```text
Factory Method
      │
      ▼
   Product
```

Example:

```ts
factory.createButton();
```

## Abstract Factory

Creates a family:

```text
Abstract Factory
      │
 ┌────┼────┐
 ▼    ▼    ▼
 A    B    C
```

Example:

```ts
factory.createButton();
factory.createCheckbox();
factory.createInput();
```

### Simple rule

> Factory Method = one product type

> Abstract Factory = multiple related product types

---

# Builder vs Factory

They answer different questions.

## Factory

> Which implementation should I create?

```ts
const payment = paymentFactory.createPayment();
```

The factory decides:

```text
StripePayment
PayPalPayment
AdyenPayment
```

## Builder

> How should I configure and construct this object?

```ts
const request = new RequestBuilder().method("POST").url("/users").timeout(5000).build();
```

### Simple rule

```text
Factory
    → WHICH object?

Builder
    → HOW should I construct it?
```

---

# Prototype vs Builder

## Prototype

```text
Existing Object
      │
      ▼
    clone()
      │
      ▼
 New Object
```

Question:

> Can I copy an existing object?

## Builder

```text
Configuration
      │
      ├── option A
      ├── option B
      ├── option C
      │
      ▼
    build()
      │
      ▼
 New Object
```

Question:

> How should I construct a new object?

---

# How They Relate to OOP

Creational patterns are closely related to core OOP concepts.

## Encapsulation

Hide implementation and creation details.

```text
Singleton
    → controls instantiation

Factory
    → hides object creation

Builder
    → hides construction process

Prototype
    → hides cloning process

Abstract Factory
    → hides family creation
```

## Abstraction

Program against interfaces:

```ts
interface Payment {
  pay(): void;
}
```

instead of concrete implementations:

```ts
class StripePayment implements Payment {}
```

## Polymorphism

A variable can represent multiple implementations:

```ts
let payment: Payment;
```

It could be:

```text
StripePayment
PayPalPayment
AdyenPayment
```

## Composition

Composition is particularly important with Abstract Factory and Dependency Injection:

```ts
class OrderService {
  constructor(private readonly paymentFactory: PaymentFactory) {}
}
```

The service **has a factory** instead of inheriting from it.

## Inheritance

Classic Factory Method frequently uses inheritance:

```ts
class EmailCreator extends NotificationCreator {}
```

However, modern TypeScript does not require inheritance for every design pattern.

---

# How They Relate to SOLID

| Pattern          | Strong SOLID Relationships                     |
| ---------------- | ---------------------------------------------- |
| Singleton        | Encapsulation; can conflict with DIP if abused |
| Factory Method   | OCP, DIP, SRP                                  |
| Abstract Factory | OCP, DIP, SRP                                  |
| Builder          | SRP                                            |
| Prototype        | SRP, OCP                                       |

## Dependency Inversion

Instead of:

```ts
class OrderService {
  private payment = new StripePayment();
}
```

use:

```ts
class OrderService {
  constructor(private readonly payment: Payment) {}
}
```

or:

```ts
class OrderService {
  constructor(private readonly factory: PaymentFactory) {}
}
```

Now high-level business logic depends on abstractions.

---

# How the Patterns Can Work Together

Patterns are not isolated. They can be combined.

## Abstract Factory + Factory Method

An Abstract Factory often contains several factory methods:

```ts
interface UIFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
  createInput(): Input;
}
```

Conceptually:

```text
Abstract Factory
    │
    ├── Factory Method → Button
    ├── Factory Method → Checkbox
    └── Factory Method → Input
```

---

## Factory + Builder

Factory chooses the implementation:

```text
Factory
   ↓
which implementation?
```

Builder configures it:

```text
Builder
   ↓
how should it be constructed?
```

Possible flow:

```text
Factory
   ↓
Stripe Request Builder
   ↓
configuration
   ↓
build()
   ↓
Stripe Request
```

---

## Prototype + Factory

A factory does not necessarily need to call `new`.

It can clone a prototype:

```ts
class DocumentFactory {
  constructor(private readonly prototype: Document) {}

  create(): Document {
    return this.prototype.clone();
  }
}
```

Flow:

```text
Factory
   ↓
Prototype
   ↓
clone()
```

---

## Prototype + Builder

Useful for templates:

```text
Existing Object
      ↓
    clone()
      ↓
Builder
      ↓
modify/configure
      ↓
final object
```

---

## Singleton + Dependency Injection

In frameworks like NestJS, dependency injection can manage singleton lifecycle for you.

Instead of:

```ts
Database.getInstance();
```

prefer a framework-managed provider when appropriate.

---

# Choosing the Right Pattern

Use this decision process:

```text
Need to create an object?
│
├── Need exactly ONE instance?
│       │
│       └── Singleton
│
├── Already have an object to copy?
│       │
│       └── Prototype
│
├── Need to construct one complex object?
│       │
│       └── Builder
│
├── Need different implementations of ONE product?
│       │
│       └── Factory Method
│
└── Need multiple compatible product types?
        │
        └── Abstract Factory
```

---

# Class Count and Complexity

There is no strict class count requirement. The pattern should be chosen based on the **problem**, not the number of classes.

## Singleton

```text
1 class
```

```text
Database
```

## Prototype

```text
Prototype
    │
    └── Concrete Prototype
```

Usually:

```text
1 interface + 1+ classes
```

## Builder

Modern:

```text
Builder → Product
```

Usually:

```text
2 main classes
```

## Factory Method

```text
Creator
│
├── Concrete Creator
└── Concrete Creator

Product
│
├── Concrete Product
└── Concrete Product
```

Potentially many classes.

## Abstract Factory

```text
Factory
│
├── Factory A
└── Factory B

Product A
├── A1
└── A2

Product B
├── B1
└── B2
```

Can introduce the most classes.

### Important

Do not think:

> "I have three classes, therefore I need Abstract Factory."

Instead ask:

> "Do these objects form a compatible product family?"

---

# Real-World Example

Imagine an e-commerce application.

## Singleton

Application configuration:

```ts
ConfigService;
```

One shared configuration instance.

---

## Factory Method

Choose a payment implementation:

```text
PaymentCreator
├── StripeCreator
├── PayPalCreator
└── AdyenCreator
```

Creates one payment product.

---

## Abstract Factory

Each payment provider has several related components:

```text
StripeFactory
├── StripePayment
├── StripeRefund
└── StripeWebhook

PayPalFactory
├── PayPalPayment
├── PayPalRefund
└── PayPalWebhook
```

The factory guarantees that the selected products belong to the same provider family.

---

## Builder

Build a complex order:

```ts
const order = new OrderBuilder().customer(user).addItem(product1, 2).addItem(product2, 1).shipping(address).discount(coupon).build();
```

---

## Prototype

Clone a product template:

```ts
const product = productTemplate.clone();
```

---

# Creational Patterns in a Modern NestJS Application

A typical architecture might look like:

```text
Application
│
├── Domain
│
├── Application Services
│
└── Infrastructure
      │
      ├── Database
      ├── Mail
      ├── Payment
      └── Storage
```

Payment could use:

```text
PaymentFactory
│
├── StripeFactory
├── PayPalFactory
└── AdyenFactory
```

An application service can depend on the abstraction:

```ts
@Injectable()
export class OrderService {
  constructor(
    @Inject(PAYMENT_FACTORY)
    private readonly paymentFactory: PaymentFactory,
  ) {}

  async checkout(order: Order) {
    const payment = this.paymentFactory.createPayment();

    await payment.pay(order.total);
  }
}
```

The business logic does not need to know whether the implementation is:

```text
Stripe
PayPal
Adyen
```

This combines:

```text
Creational Pattern
        +
OOP Abstraction
        +
Dependency Injection
        +
Dependency Inversion
```

---

# Final Cheat Sheet

```text
┌────────────────────────────────────────────────────────────┐
│                 CREATIONAL DESIGN PATTERNS                  │
├───────────────┬────────────────────────────────────────────┤
│ Singleton     │ ONE INSTANCE                               │
│               │ "Only one object should exist."            │
├───────────────┼────────────────────────────────────────────┤
│ Prototype     │ COPY                                       │
│               │ "Clone an existing object."                │
├───────────────┼────────────────────────────────────────────┤
│ Builder       │ CONSTRUCTION                               │
│               │ "Build one complex object step-by-step."   │
├───────────────┼────────────────────────────────────────────┤
│ Factory       │ ONE PRODUCT TYPE                           │
│ Method        │ "Which implementation should I create?"   │
├───────────────┼────────────────────────────────────────────┤
│ Abstract      │ PRODUCT FAMILY                             │
│ Factory       │ "Which compatible family should I use?"   │
└───────────────┴────────────────────────────────────────────┘
```

## The Five Sentences to Memorize

### Singleton

> **There should be only one.**

### Prototype

> **I already have one; copy it.**

### Builder

> **I need to construct this carefully.**

### Factory Method

> **I need one product, but its concrete type can vary.**

### Abstract Factory

> **I need a whole compatible family of products.**

---

# The Ultimate Mental Model

```text
                  OBJECT CREATION
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
   Instance?        Existing object?   New object?
        │               │                │
        ▼               ▼                │
   Singleton         Prototype          │
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                         Complex build?        Implementation?
                              │                     │
                              ▼                     ▼
                           Builder           ┌──────┴──────┐
                                             │             │
                                        One product    Product family
                                             │             │
                                             ▼             ▼
                                      Factory Method  Abstract Factory
```

## One-line summary

```text
Singleton       → ONE INSTANCE
Prototype       → COPY
Builder         → HOW TO BUILD
Factory Method  → WHICH PRODUCT
Abstract Factory→ WHICH PRODUCT FAMILY
```

---

## Pattern Relationships

```text
                         Creational Patterns
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
        Singleton           Factories            Builder
            │                   │                   │
            │             ┌─────┴─────┐             │
            │             │           │             │
            │        Factory Method   │             │
            │                        Abstract       │
            │                        Factory        │
            │                           │           │
            └──────────────┬────────────┴───────────┘
                           │
                       Prototype
```

The most important conceptual difference is:

```text
Factory Method
    ↓
Which concrete object?

Abstract Factory
    ↓
Which family of compatible objects?

Builder
    ↓
How do I construct one complex object?

Prototype
    ↓
How do I copy an existing object?

Singleton
    ↓
How do I ensure there is only one instance?
```

---

## Recommended Learning Order

For understanding the patterns rather than memorizing them:

```text
1. OOP fundamentals
       ↓
2. Encapsulation / Abstraction / Polymorphism
       ↓
3. SOLID
       ↓
4. Singleton
       ↓
5. Factory Method
       ↓
6. Abstract Factory
       ↓
7. Builder
       ↓
8. Prototype
       ↓
9. Combine patterns
       ↓
10. Apply them in real TypeScript/NestJS projects
```

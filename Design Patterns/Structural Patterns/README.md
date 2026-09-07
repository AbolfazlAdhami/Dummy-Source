# GoF Structural Design Patterns — Complete Study Notes

> A practical, TypeScript/NestJS-oriented guide to all seven GoF Structural Design Patterns.

---

## Table of Contents

1. [What Are Structural Patterns?](#what-are-structural-patterns)
2. [Structural Patterns at a Glance](#structural-patterns-at-a-glance)
3. [Adapter](#1-adapter)
4. [Bridge](#2-bridge)
5. [Composite](#3-composite)
6. [Decorator](#4-decorator)
7. [Facade](#5-facade)
8. [Flyweight](#6-flyweight)
9. [Proxy](#7-proxy)
10. [Comparing All Seven Patterns](#comparing-all-seven-patterns)
11. [NestJS Mapping](#nestjs-mapping)
12. [How to Recognize the Pattern](#how-to-recognize-the-pattern)
13. [Common Confusions](#common-confusions)
14. [Learning Checklist](#learning-checklist)

---

# What Are Structural Patterns?

Structural Design Patterns explain **how classes and objects are composed** to form larger, flexible structures.

The GoF defines seven Structural Patterns:

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

The central question is:

> **How can I compose objects/classes without creating a rigid design?**

A useful mental model:

```text
Adapter   → Convert an interface
Bridge    → Separate abstraction from implementation
Composite → Build a hierarchy/tree
Decorator → Add behavior through wrapping
Facade    → Simplify a complex subsystem
Flyweight → Share common state
Proxy     → Control access to an object
```

---

# Structural Patterns at a Glance

| Pattern | Main Problem | Main Idea |
|---|---|---|
| Adapter | Interfaces don't match | Translate one interface into another |
| Bridge | Abstraction and implementation vary independently | Separate the two dimensions |
| Composite | Need to treat objects and groups uniformly | Build recursive tree structures |
| Decorator | Need to add behavior dynamically | Wrap an object |
| Facade | Subsystem is complicated | Expose a simpler interface |
| Flyweight | Too many similar objects consume memory | Share intrinsic state |
| Proxy | Access to an object needs control | Put a substitute in front of it |

---

# 1. Adapter

## Definition

> **Adapter converts the interface of a class into another interface that clients expect.**

Use Adapter when two components are useful together but their interfaces are incompatible.

### Problem

Suppose our application expects:

```ts
interface PaymentGateway {
  pay(amount: number): Promise<void>;
}
```

But a third-party library provides:

```ts
class StripeSDK {
  async makePayment(amountInCents: number) {
    console.log(`Stripe payment: ${amountInCents}`);
  }
}
```

The interfaces don't match.

### Solution

Create an Adapter:

```ts
class StripePaymentAdapter implements PaymentGateway {
  constructor(private readonly stripe: StripeSDK) {}

  async pay(amount: number) {
    await this.stripe.makePayment(amount * 100);
  }
}
```

Now the application only knows:

```ts
PaymentGateway
```

and does not depend directly on the third-party API.

## Structure

```text
Client
  │
  ▼
Target Interface
  │
  ▼
Adapter
  │
  ▼
Adaptee
```

## NestJS Example

```ts
export const PAYMENT_GATEWAY = Symbol('PAYMENT_GATEWAY');

export interface PaymentGateway {
  pay(amount: number): Promise<void>;
}
```

Third-party class:

```ts
export class StripeSDK {
  async makePayment(amountInCents: number) {
    console.log(`Stripe payment: ${amountInCents}`);
  }
}
```

Adapter:

```ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class StripePaymentAdapter implements PaymentGateway {
  constructor(private readonly stripe: StripeSDK) {}

  async pay(amount: number) {
    await this.stripe.makePayment(amount * 100);
  }
}
```

Provider:

```ts
@Module({
  providers: [
    StripeSDK,
    {
      provide: PAYMENT_GATEWAY,
      inject: [StripeSDK],
      useFactory: (stripe: StripeSDK) => {
        return new StripePaymentAdapter(stripe);
      },
    },
  ],
  exports: [PAYMENT_GATEWAY],
})
export class PaymentModule {}
```

Client:

```ts
@Injectable()
export class CheckoutService {
  constructor(
    @Inject(PAYMENT_GATEWAY)
    private readonly paymentGateway: PaymentGateway,
  ) {}

  async checkout() {
    await this.paymentGateway.pay(100);
  }
}
```

## When to Use

- Integrating third-party SDKs
- Legacy APIs
- Migrating from one provider to another
- Supporting multiple external services
- Normalizing inconsistent APIs

## Adapter vs Facade

```text
Adapter
  ↓
Changes/bridges an interface

Facade
  ↓
Simplifies access to a subsystem
```

---

# 2. Bridge

## Definition

> **Bridge separates an abstraction from its implementation so that the two can vary independently.**

The key idea is **two independent dimensions**.

### Problem

Imagine notifications can be:

- Email
- SMS

And notification types can be:

- Alert
- Marketing
- Security

Without Bridge, you can end up with:

```text
EmailAlert
EmailMarketing
EmailSecurity

SMSAlert
SMSMarketing
SMSSecurity
```

If there are 4 notification types and 5 delivery channels:

```text
4 × 5 = 20 classes
```

### Solution

Separate:

```text
Abstraction
    +
Implementation
```

## Structure

```text
Notification
     │
     ├─────────────── uses ───────────────► NotificationSender
     │                                          │
     │                                          ├── EmailSender
     │                                          └── SmsSender
     │
     ├── AlertNotification
     └── MarketingNotification
```

## TypeScript

Implementation:

```ts
interface MessageSender {
  send(message: string): Promise<void>;
}

class EmailSender implements MessageSender {
  async send(message: string) {
    console.log(`Email: ${message}`);
  }
}

class SmsSender implements MessageSender {
  async send(message: string) {
    console.log(`SMS: ${message}`);
  }
}
```

Abstraction:

```ts
abstract class Notification {
  constructor(
    protected readonly sender: MessageSender,
  ) {}

  abstract notify(message: string): Promise<void>;
}
```

Refined abstractions:

```ts
class AlertNotification extends Notification {
  async notify(message: string) {
    await this.sender.send(`[ALERT] ${message}`);
  }
}

class MarketingNotification extends Notification {
  async notify(message: string) {
    await this.sender.send(`[MARKETING] ${message}`);
  }
}
```

Usage:

```ts
const email = new EmailSender();
const sms = new SmsSender();

const alertByEmail = new AlertNotification(email);
const alertBySms = new AlertNotification(sms);

await alertByEmail.notify('Server is down');
await alertBySms.notify('Server is down');
```

No `EmailAlert`, `SmsAlert`, etc. are required.

## NestJS Example

```ts
export interface NotificationSender {
  send(message: string): Promise<void>;
}
```

Implementations:

```ts
@Injectable()
export class EmailSender implements NotificationSender {
  async send(message: string) {
    console.log(`EMAIL: ${message}`);
  }
}
```

```ts
@Injectable()
export class SmsSender implements NotificationSender {
  async send(message: string) {
    console.log(`SMS: ${message}`);
  }
}
```

Abstraction:

```ts
@Injectable()
export class AlertNotification {
  constructor(
    private readonly sender: NotificationSender,
  ) {}

  async notify(message: string) {
    return this.sender.send(`[ALERT] ${message}`);
  }
}
```

## When to Use

Use Bridge when:

- You have two independent dimensions
- Both dimensions are expected to change
- Inheritance would create a class explosion
- You want composition instead of a large inheritance hierarchy

## Bridge vs Adapter

```text
Adapter
  → Existing interfaces don't match.

Bridge
  → You design the system so two dimensions remain independent.
```

---

# 3. Composite

## Definition

> **Composite lets clients treat individual objects and compositions of objects uniformly.**

Composite is ideal for **tree structures**.

Examples:

- File systems
- Organization charts
- UI component trees
- Menus
- Permission trees
- Product categories

## Structure

```text
Component
   │
   ├── Leaf
   │
   └── Composite
          │
          ├── Leaf
          ├── Leaf
          └── Composite
```

## Example: File System

Common interface:

```ts
interface FileSystemItem {
  getSize(): number;
}
```

Leaf:

```ts
class FileItem implements FileSystemItem {
  constructor(
    private readonly size: number,
  ) {}

  getSize() {
    return this.size;
  }
}
```

Composite:

```ts
class Directory implements FileSystemItem {
  private readonly children: FileSystemItem[] = [];

  add(item: FileSystemItem) {
    this.children.push(item);
  }

  getSize() {
    return this.children.reduce(
      (total, child) => total + child.getSize(),
      0,
    );
  }
}
```

Usage:

```ts
const file1 = new FileItem(100);
const file2 = new FileItem(200);

const folder = new Directory();

folder.add(file1);
folder.add(file2);

console.log(folder.getSize()); // 300
```

The client doesn't need to know whether it has a file or directory.

## NestJS Example: Permission Tree

```ts
export interface PermissionNode {
  check(userId: string): boolean;
}
```

Leaf:

```ts
@Injectable()
export class Permission implements PermissionNode {
  constructor(
    private readonly allowedUsers: Set<string>,
  ) {}

  check(userId: string) {
    return this.allowedUsers.has(userId);
  }
}
```

Composite:

```ts
@Injectable()
export class PermissionGroup implements PermissionNode {
  constructor(
    private readonly permissions: PermissionNode[],
  ) {}

  check(userId: string) {
    return this.permissions.some(
      permission => permission.check(userId),
    );
  }
}
```

## Important Concept

Composite is about **part-whole hierarchies**.

The client can use:

```ts
Component
```

without caring whether the concrete object is:

```text
Leaf
```

or:

```text
Composite
```

## When to Use

- Recursive structures
- Tree structures
- Nested UI
- File systems
- Menus
- Organizations
- Permission hierarchies

## Composite vs Decorator

```text
Composite
  → One object contains many children.

Decorator
  → One object wraps another object.
```

---

# 4. Decorator

## Definition

> **Decorator attaches additional responsibilities to an object dynamically by wrapping it.**

The important property is:

```text
Decorator
    implements same interface
           │
           ▼
      wraps component
```

## Basic Structure

```text
Client
  │
  ▼
Component
  ▲
  │
Decorator
  │
  ▼
Concrete Component
```

## TypeScript Example

Interface:

```ts
interface ProductService {
  getProduct(id: string): Promise<any>;
}
```

Concrete component:

```ts
class DatabaseProductService implements ProductService {
  async getProduct(id: string) {
    return {
      id,
      name: 'Laptop',
    };
  }
}
```

Logging decorator:

```ts
class LoggingProductService implements ProductService {
  constructor(
    private readonly service: ProductService,
  ) {}

  async getProduct(id: string) {
    console.log(`Getting product ${id}`);

    const result = await this.service.getProduct(id);

    console.log('Product loaded');

    return result;
  }
}
```

Caching decorator:

```ts
class CachingProductService implements ProductService {
  private readonly cache = new Map<string, any>();

  constructor(
    private readonly service: ProductService,
  ) {}

  async getProduct(id: string) {
    const cached = this.cache.get(id);

    if (cached) {
      return cached;
    }

    const result = await this.service.getProduct(id);

    this.cache.set(id, result);

    return result;
  }
}
```

Composition:

```ts
const database = new DatabaseProductService();

const cache = new CachingProductService(database);

const logging = new LoggingProductService(cache);

await logging.getProduct('1');
```

Result:

```text
Logging
   ↓
Caching
   ↓
Database
```

## NestJS Example

Token:

```ts
export const PRODUCT_SERVICE = Symbol('PRODUCT_SERVICE');
```

Interface:

```ts
export interface ProductService {
  getProduct(id: string): Promise<any>;
}
```

Concrete service:

```ts
@Injectable()
export class DatabaseProductService implements ProductService {
  async getProduct(id: string) {
    return {
      id,
      name: 'Laptop',
    };
  }
}
```

Logging decorator:

```ts
@Injectable()
export class LoggingProductService implements ProductService {
  constructor(
    private readonly service: ProductService,
  ) {}

  async getProduct(id: string) {
    console.log(`GET product ${id}`);

    return this.service.getProduct(id);
  }
}
```

Caching decorator:

```ts
@Injectable()
export class CachingProductService implements ProductService {
  private readonly cache = new Map<string, any>();

  constructor(
    private readonly service: ProductService,
  ) {}

  async getProduct(id: string) {
    const cached = this.cache.get(id);

    if (cached) {
      return cached;
    }

    const result = await this.service.getProduct(id);

    this.cache.set(id, result);

    return result;
  }
}
```

Provider composition:

```ts
@Module({
  providers: [
    DatabaseProductService,
    {
      provide: PRODUCT_SERVICE,
      inject: [DatabaseProductService],
      useFactory: (
        databaseProductService: DatabaseProductService,
      ) => {
        const metrics = new MetricsProductService(
          databaseProductService,
        );

        const cache = new CachingProductService(metrics);

        const logging = new LoggingProductService(cache);

        return logging;
      },
    },
  ],
  exports: [PRODUCT_SERVICE],
})
export class ProductModule {}
```

Controller:

```ts
@Controller('products')
export class ProductController {
  constructor(
    @Inject(PRODUCT_SERVICE)
    private readonly productService: ProductService,
  ) {}

  @Get(':id')
  getProduct(@Param('id') id: string) {
    return this.productService.getProduct(id);
  }
}
```

## Decorator vs NestJS Decorators

This is important:

```ts
@Injectable()
@Controller()
@Get()
```

are **language/framework decorators**, not necessarily examples of the GoF Decorator Pattern.

NestJS Interceptors are conceptually closer to the GoF Decorator because they wrap execution and add behavior, but they should not automatically be labeled as GoF Decorators.

## When to Use

- Logging
- Metrics
- Caching
- Retry
- Authorization
- Transactions
- Compression
- Additional behavior around an existing service

## Decorator vs Proxy

```text
Decorator
  → Main intent: add responsibilities/behavior.

Proxy
  → Main intent: control access or provide indirection.
```

---

# 5. Facade

## Definition

> **Facade provides a simple interface to a complex subsystem.**

Facade does not necessarily add behavior to one object.

Instead, it hides coordination between multiple services.

## Problem

Checkout might require:

```text
OrderService
InventoryService
PaymentService
ShippingService
NotificationService
```

Without a Facade:

```text
Controller
  ├── OrderService
  ├── InventoryService
  ├── PaymentService
  ├── ShippingService
  └── NotificationService
```

The controller knows too much.

## Solution

```text
Controller
    ↓
CheckoutFacade
    ↓
 ┌───────────────┬──────────────┬─────────────┐
Order          Inventory      Payment
                                  │
                              Shipping
                                  │
                            Notification
```

## NestJS Structure

```text
src/
└── checkout/
    ├── checkout.controller.ts
    ├── checkout.facade.ts
    └── services/
        ├── order.service.ts
        ├── payment.service.ts
        ├── inventory.service.ts
        ├── shipping.service.ts
        └── notification.service.ts
```

Facade:

```ts
@Injectable()
export class CheckoutFacade {
  constructor(
    private readonly orderService: OrderService,
    private readonly inventoryService: InventoryService,
    private readonly paymentService: PaymentService,
    private readonly shippingService: ShippingService,
    private readonly notificationService: NotificationService,
  ) {}

  async checkout(data: {
    userId: string;
    productId: string;
    quantity: number;
  }) {
    const order =
      await this.orderService.createOrder(data);

    await this.inventoryService.reserve(
      order.productId,
      order.quantity,
    );

    const payment =
      await this.paymentService.charge(
        order.userId,
        order.total,
      );

    const shipment =
      await this.shippingService.createShipment(
        order.id,
      );

    await this.notificationService
      .sendOrderConfirmation(
        order.userId,
        order.id,
      );

    return {
      order,
      payment,
      shipment,
    };
  }
}
```

Controller:

```ts
@Controller('checkout')
export class CheckoutController {
  constructor(
    private readonly checkoutFacade: CheckoutFacade,
  ) {}

  @Post()
  checkout(@Body() body: any) {
    return this.checkoutFacade.checkout(body);
  }
}
```

## Facade vs Use Case

In Clean Architecture, an Application Service or Use Case can look structurally similar to a Facade.

But the intent differs:

```text
Facade
  → Simplifies access to a subsystem.

Use Case
  → Represents an application/business operation.
```

A class can technically resemble both, but the design intent matters.

## When to Use

- Complex workflows
- Multiple services involved in one operation
- Simplifying controllers
- Hiding subsystem complexity
- Providing a stable API over changing internals

---

# 6. Flyweight

## Definition

> **Flyweight minimizes memory usage by sharing common intrinsic state between many objects.**

Flyweight becomes useful when you have a **large number of similar objects**.

## Example

Imagine a game rendering:

```text
100,000 trees
```

Each tree has:

```text
type
texture
color
x
y
```

But:

```text
type
texture
color
```

may be identical for thousands of trees.

Only:

```text
x
y
```

changes.

So separate the state.

## Intrinsic vs Extrinsic State

### Intrinsic State

Shared:

```text
type
texture
color
```

### Extrinsic State

Unique:

```text
x
y
```

Diagram:

```text
Tree
│
├── Intrinsic State
│   ├── type
│   ├── texture
│   └── color
│
└── Extrinsic State
    ├── x
    └── y
```

## TypeScript Example

Flyweight:

```ts
class TreeType {
  constructor(
    public readonly name: string,
    public readonly texture: string,
    public readonly color: string,
  ) {}

  draw(x: number, y: number) {
    console.log(
      `Drawing ${this.name} at (${x}, ${y})`,
    );
  }
}
```

Context:

```ts
class Tree {
  constructor(
    private readonly x: number,
    private readonly y: number,
    private readonly type: TreeType,
  ) {}

  draw() {
    this.type.draw(this.x, this.y);
  }
}
```

Factory:

```ts
class TreeTypeFactory {
  private readonly treeTypes =
    new Map<string, TreeType>();

  getTreeType(
    name: string,
    texture: string,
    color: string,
  ): TreeType {
    const key = `${name}:${texture}:${color}`;

    if (!this.treeTypes.has(key)) {
      this.treeTypes.set(
        key,
        new TreeType(
          name,
          texture,
          color,
        ),
      );
    }

    return this.treeTypes.get(key)!;
  }
}
```

Usage:

```ts
const factory = new TreeTypeFactory();

const oak1 = factory.getTreeType(
  'oak',
  'oak.png',
  'green',
);

const oak2 = factory.getTreeType(
  'oak',
  'oak.png',
  'green',
);

console.log(oak1 === oak2); // true
```

The same flyweight instance is shared.

## NestJS Example: Notification Types

Flyweight:

```ts
export class NotificationType {
  constructor(
    public readonly type: string,
    public readonly template: string,
    public readonly icon: string,
  ) {}

  render(
    userId: string,
    orderId: string,
  ) {
    return {
      userId,
      orderId,
      template: this.template,
      icon: this.icon,
    };
  }
}
```

Factory:

```ts
@Injectable()
export class NotificationTypeFactory {
  private readonly types =
    new Map<string, NotificationType>();

  get(
    type: string,
    template: string,
    icon: string,
  ): NotificationType {
    const existing = this.types.get(type);

    if (existing) {
      return existing;
    }

    const notificationType =
      new NotificationType(
        type,
        template,
        icon,
      );

    this.types.set(type, notificationType);

    return notificationType;
  }
}
```

Context:

```ts
export class Notification {
  constructor(
    public readonly userId: string,
    public readonly orderId: string,
    public readonly type: NotificationType,
  ) {}

  send() {
    return this.type.render(
      this.userId,
      this.orderId,
    );
  }
}
```

Service:

```ts
@Injectable()
export class NotificationService {
  constructor(
    private readonly factory: NotificationTypeFactory,
  ) {}

  createOrderNotification(
    userId: string,
    orderId: string,
  ) {
    const type = this.factory.get(
      'ORDER_CREATED',
      'order-created',
      'shopping-cart',
    );

    return new Notification(
      userId,
      orderId,
      type,
    );
  }
}
```

## Flyweight vs Singleton

```text
Singleton
  → One instance of a class/application-wide scope.

Flyweight
  → Shared intrinsic state between many objects.
```

You can have:

```text
Oak Flyweight
Pine Flyweight
Birch Flyweight
```

So Flyweight does not mean "there is only one object."

## Flyweight vs Cache

Both often use:

```ts
Map
```

But the purpose differs:

```text
Cache
  → Store/reuse previous results.

Flyweight
  → Share reusable object state.
```

## Flyweight vs Prototype

```text
Prototype
  → Clone an existing object.

Flyweight
  → Reuse the same shared object.
```

## When to Use

- Game objects
- Text editor characters
- Icons
- Fonts
- Maps
- Large UI systems
- Product categories
- Notification templates
- Permission definitions
- Database metadata

---

# 7. Proxy

## Definition

> **Proxy provides a substitute object that controls access to a real object.**

The Proxy usually exposes the **same interface** as the real subject.

## Structure

```text
Client
   │
   ▼
 Proxy
   │
   ▼
Real Subject
```

The client doesn't need to know whether it is communicating with:

```text
Proxy
```

or:

```text
Real Subject
```

## TypeScript Example

Interface:

```ts
interface UserService {
  getUser(id: string): Promise<User>;
}

interface User {
  id: string;
  name: string;
}
```

Real service:

```ts
class RealUserService implements UserService {
  async getUser(id: string): Promise<User> {
    console.log(
      'Fetching user from database...',
    );

    return {
      id,
      name: 'Abolfazl',
    };
  }
}
```

Proxy:

```ts
class UserServiceProxy implements UserService {
  constructor(
    private readonly realService: UserService,
  ) {}

  async getUser(id: string) {
    console.log('Checking permission...');

    const user =
      await this.realService.getUser(id);

    console.log('Access granted');

    return user;
  }
}
```

## Types of Proxy

### 1. Protection Proxy

Controls access:

```text
Client
  ↓
Authorization Proxy
  ↓
Real Service
```

Example:

```ts
if (!hasPermission) {
  throw new ForbiddenException();
}
```

### 2. Virtual Proxy

Delays creation/loading of an expensive object.

```text
Client
  ↓
Virtual Proxy
  ↓
Heavy Object
```

Useful for:

- Large images
- Expensive resources
- Heavy database objects

### 3. Remote Proxy

Represents an object located somewhere else.

```text
Client
  ↓
Proxy
  ↓
HTTP / TCP / gRPC / Redis / NATS
  ↓
Remote Service
```

### 4. Caching Proxy

Caches responses:

```ts
class UserCacheProxy implements UserService {
  private readonly cache =
    new Map<string, User>();

  constructor(
    private readonly service: UserService,
  ) {}

  async getUser(id: string) {
    const cached = this.cache.get(id);

    if (cached) {
      console.log('Cache hit');
      return cached;
    }

    const user =
      await this.service.getUser(id);

    this.cache.set(id, user);

    return user;
  }
}
```

## NestJS Protection Proxy

Interface:

```ts
export interface IUserService {
  getUser(id: string): Promise<any>;
}
```

Real service:

```ts
@Injectable()
export class UserService
  implements IUserService
{
  async getUser(id: string) {
    console.log('Query database');

    return {
      id,
      name: 'Abolfazl',
    };
  }
}
```

Proxy:

```ts
@Injectable()
export class UserServiceProxy
  implements IUserService
{
  constructor(
    private readonly userService: UserService,
  ) {}

  async getUser(id: string) {
    const hasPermission = true;

    if (!hasPermission) {
      throw new ForbiddenException(
        'Access denied',
      );
    }

    console.log(
      'Proxy: permission granted',
    );

    return this.userService.getUser(id);
  }
}
```

Provider:

```ts
export const USER_SERVICE =
  Symbol('USER_SERVICE');

@Module({
  providers: [
    UserService,
    {
      provide: USER_SERVICE,
      inject: [UserService],
      useFactory: (
        userService: UserService,
      ) => {
        return new UserServiceProxy(
          userService,
        );
      },
    },
  ],
  controllers: [UserController],
})
export class UserModule {}
```

Controller:

```ts
@Controller('users')
export class UserController {
  constructor(
    @Inject(USER_SERVICE)
    private readonly userService: IUserService,
  ) {}

  @Get(':id')
  getUser(
    @Param('id') id: string,
  ) {
    return this.userService.getUser(id);
  }
}
```

## Proxy vs Decorator

Both commonly look like:

```text
Client
  ↓
Wrapper
  ↓
Real Object
```

But intent differs:

```text
Decorator
  → Add responsibilities.

Proxy
  → Control access / indirection / lifecycle / remote communication.
```

## Proxy vs Adapter

```text
Adapter
  → Changes interface.

Proxy
  → Usually preserves the interface.
```

## Proxy vs Facade

```text
Proxy
  → Represents/protects one target.

Facade
  → Simplifies multiple subsystem components.
```

## NestJS and Proxy Concepts

NestJS features that can resemble Proxy structurally or conceptually include:

- Guards
- Interceptors
- Custom providers
- Lazy loading
- Microservice client proxies

For example, a microservice client can conceptually act as:

```text
Controller
    │
    ▼
ClientProxy
    │
    │ TCP / Redis / NATS / ...
    ▼
Remote Microservice
```

---

# Comparing All Seven Patterns

## Adapter

Question:

> "How do I make these incompatible interfaces work together?"

```text
A → Adapter → B
```

## Bridge

Question:

> "How do I keep two dimensions independent?"

```text
Abstraction → Implementation
```

## Composite

Question:

> "How do I treat an object and a group of objects uniformly?"

```text
Tree
├── Leaf
├── Leaf
└── Composite
```

## Decorator

Question:

> "How do I add behavior without modifying the original class?"

```text
Decorator
   ↓
Component
```

## Facade

Question:

> "How do I make a complicated subsystem easy to use?"

```text
Client
  ↓
Facade
  ↓
Many services
```

## Flyweight

Question:

> "How do I avoid creating thousands of identical pieces of state?"

```text
Many objects
      ↓
Shared intrinsic state
```

## Proxy

Question:

> "How do I control access to an object?"

```text
Client
  ↓
Proxy
  ↓
Real object
```

---

# The Most Important Differences

## Adapter vs Bridge

```text
Adapter
  → Usually applied because existing interfaces are incompatible.

Bridge
  → Usually designed from the beginning to separate dimensions.
```

## Adapter vs Decorator

```text
Adapter
  → Changes interface.

Decorator
  → Preserves interface and adds behavior.
```

## Decorator vs Proxy

```text
Decorator
  → Add responsibilities.

Proxy
  → Control access.
```

## Facade vs Adapter

```text
Facade
  → Simplifies a subsystem.

Adapter
  → Translates an interface.
```

## Composite vs Decorator

```text
Composite
  → Contains multiple children.

Decorator
  → Wraps one component.
```

## Flyweight vs Singleton

```text
Singleton
  → One shared instance.

Flyweight
  → Shared intrinsic state.
```

## Proxy vs Facade

```text
Proxy
  → One representative/substitute for a target.

Facade
  → One simplified entry point to a subsystem.
```

---

# NestJS Mapping

These are conceptual mappings, not claims that NestJS internally implements every GoF pattern exactly.

| GoF Pattern | Common NestJS Concept |
|---|---|
| Adapter | Provider wrapping third-party SDK |
| Bridge | Strategy/provider composition |
| Composite | Nested providers/domain trees |
| Decorator | Interceptors / wrapper services |
| Facade | Application service / orchestration service |
| Flyweight | Singleton-scoped cached factory |
| Proxy | Guards, interceptors, client proxies, wrapper providers |

The important rule is:

> Do not identify a pattern merely because the framework has a similarly named feature. Identify the **design intent**.

---

# How to Recognize the Pattern

When reading code, ask these questions.

## 1. Do interfaces not match?

```text
YES → Adapter
```

## 2. Are there two independent dimensions?

```text
YES → Bridge
```

Example:

```text
Notification type × Delivery channel
```

## 3. Is the data hierarchical or recursive?

```text
YES → Composite
```

Example:

```text
Folder
 ├── File
 └── Folder
      └── File
```

## 4. Am I wrapping an object to add behavior?

```text
YES → Decorator
```

## 5. Am I hiding multiple services behind one simpler API?

```text
YES → Facade
```

## 6. Are thousands/millions of objects sharing the same state?

```text
YES → Flyweight
```

## 7. Am I controlling access to another object?

```text
YES → Proxy
```

---

# A Practical Mental Model

Memorize these seven verbs:

```text
Adapter   → TRANSLATE
Bridge    → SEPARATE
Composite → COMPOSE
Decorator → EXTEND
Facade    → SIMPLIFY
Flyweight → SHARE
Proxy     → CONTROL
```

This is one of the easiest ways to remember the Structural Patterns.

---

# Structural Patterns in One Diagram

```text
                    STRUCTURAL PATTERNS
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    Interfaces          Composition          Access
        │                   │                   │
   ┌────┴────┐        ┌─────┼─────┐             │
   │         │        │     │     │             │
Adapter    Bridge   Composite Decorator       Proxy
                       │
                    Facade
                       │
                    Flyweight
```

A more useful classification:

```text
INTERFACE
  Adapter
  Bridge

STRUCTURE / COMPOSITION
  Composite
  Decorator
  Facade

MEMORY / SHARING
  Flyweight

ACCESS / INDIRECTION
  Proxy
```

---

# Example: One E-Commerce System Using All Seven

A mature e-commerce application can potentially use all seven patterns.

## Adapter

Integrate Stripe:

```text
PaymentGateway
      ↓
StripeAdapter
      ↓
Stripe SDK
```

## Bridge

Notification type and delivery channel:

```text
Alert ──────┐
            ├── Email
Marketing ──┤
            ├── SMS
Security ───┘
```

## Composite

Category hierarchy:

```text
Electronics
├── Phones
│   ├── iPhone
│   └── Pixel
└── Laptops
    ├── MacBook
    └── ThinkPad
```

## Decorator

Product service:

```text
Logging
  ↓
Caching
  ↓
Metrics
  ↓
Database
```

## Facade

Checkout:

```text
CheckoutFacade
    ├── Order
    ├── Inventory
    ├── Payment
    ├── Shipping
    └── Notification
```

## Flyweight

Shared product metadata:

```text
10,000 products
      ↓
Shared category/metadata definitions
```

## Proxy

Protected/cached remote service:

```text
Controller
   ↓
UserServiceProxy
   ↓
UserService
```

---

# Common Design Mistakes

## Mistake 1: Calling every wrapper a Decorator

A wrapper can be:

- Adapter
- Decorator
- Proxy

Look at the intent.

```text
Translate interface → Adapter
Add behavior → Decorator
Control access → Proxy
```

## Mistake 2: Calling every service coordinator a Facade

A service coordinating business rules may be:

- Application Service
- Use Case
- Domain Service
- Facade

Look at its responsibility and architectural layer.

## Mistake 3: Using Flyweight without measuring

Flyweight introduces:

- Factory/cache complexity
- Shared mutable-state concerns
- Identity considerations

Use it when object count/state duplication makes the tradeoff worthwhile.

## Mistake 4: Using inheritance where Bridge is better

If you see:

```text
EmailAlert
EmailMarketing
EmailSecurity
SmsAlert
SmsMarketing
SmsSecurity
```

ask whether the dimensions can be separated.

## Mistake 5: Confusing Proxy and Decorator

The implementation may look almost identical.

The deciding factor is **intent**, not syntax.

---

# Implementation Checklist

When implementing a Structural Pattern, identify:

## 1. Client

Who uses the abstraction?

## 2. Target/Component

What interface does the client depend on?

## 3. Concrete implementation

What actually performs the work?

## 4. Relationship

Is the relationship:

```text
translate?
separate?
contain?
wrap?
simplify?
share?
control?
```

## 5. Composition

Prefer composition when the pattern calls for it:

```ts
constructor(
  private readonly dependency: Interface,
) {}
```

rather than building large inheritance trees.

---

# Final Cheat Sheet

```text
┌────────────┬────────────────────────────────────────────┐
│ Adapter    │ Make incompatible interfaces compatible   │
├────────────┼────────────────────────────────────────────┤
│ Bridge     │ Separate abstraction from implementation  │
├────────────┼────────────────────────────────────────────┤
│ Composite  │ Treat trees/parts and wholes uniformly    │
├────────────┼────────────────────────────────────────────┤
│ Decorator  │ Add behavior by wrapping                  │
├────────────┼────────────────────────────────────────────┤
│ Facade     │ Simplify a complex subsystem              │
├────────────┼────────────────────────────────────────────┤
│ Flyweight  │ Share common intrinsic state              │
├────────────┼────────────────────────────────────────────┤
│ Proxy      │ Control access to a target                │
└────────────┴────────────────────────────────────────────┘
```

## One-line memory trick

```text
Adapter   = Translate
Bridge    = Separate
Composite = Tree
Decorator = Wrap
Facade    = Simplify
Flyweight = Share
Proxy     = Control
```

---

# Recommended Study Order

For practical software engineering, study them in this order:

```text
1. Adapter
      ↓
2. Decorator
      ↓
3. Proxy
      ↓
4. Facade
      ↓
5. Composite
      ↓
6. Bridge
      ↓
7. Flyweight
```

Why?

Because the first four are especially common in application/backend development:

```text
Adapter   → integrations
Decorator → cross-cutting behavior
Proxy     → access/caching/remote calls
Facade    → service orchestration
```

Then move into:

```text
Composite → recursive structures
Bridge    → architecture with independent dimensions
Flyweight → memory optimization
```

---

# Final Mental Model

When reverse-engineering a TypeScript/NestJS codebase, don't search for class names like `Adapter`, `Proxy`, or `Facade`.

Instead, search for **relationships**:

```text
Does one class translate another API?
        ↓
      Adapter

Does one abstraction delegate to a replaceable implementation?
        ↓
      Bridge

Does one object contain a collection of objects of the same abstraction?
        ↓
      Composite

Does one service wrap another service with the same interface?
        ↓
      Decorator / Proxy

Does one service coordinate several subsystems behind one API?
        ↓
      Facade

Does a factory reuse identical immutable/shared objects?
        ↓
      Flyweight

Does a substitute control access to a real object?
        ↓
      Proxy
```

The most important principle is:

> **Design patterns are about intent and object relationships, not class names.**

That principle is especially important when reverse-engineering real NestJS applications, because production code rarely names classes exactly after the GoF pattern.

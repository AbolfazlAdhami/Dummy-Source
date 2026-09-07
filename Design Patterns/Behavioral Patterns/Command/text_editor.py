from abc import ABC, abstractmethod

# 1. Receiver: Holds the core business logic (the document buffer)


class TextDocument:
    def __init__(self):
        self.text = ""

    def write(self, text_to_insert: str, position: int):
        self.text = self.text[:position] + \
            text_to_insert + self.text[position:]

    def delete(self, position: int, length: int) -> str:
        deleted_text = self.text[position: position + length]
        self.text = self.text[:position] + self.text[position + length:]
        return deleted_text

# 2. Command Interface


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# 3. Concrete Commands


class InsertTextCommand(Command):
    def __init__(self, doc: TextDocument, text: str, position: int):
        self.doc = doc
        self.text = text
        self.position = position

    def execute(self):
        self.doc.write(self.text, self.position)

    def undo(self):
        self.doc.delete(self.position, len(self.text))


class DeleteTextCommand(Command):
    def __init__(self, doc: TextDocument, position: int, length: int):
        self.doc = doc
        self.position = position
        self.length = length
        self._deleted_text = ""  # State stored for undoing

    def execute(self):
        self._deleted_text = self.doc.delete(self.position, self.length)

    def undo(self):
        # Restore exact text that was deleted at the exact position
        self.doc.write(self._deleted_text, self.position)

# Macro Command: Groups multiple commands into a single batch


class MacroCommand(Command):
    def __init__(self, commands: list[Command]):
        self.commands = commands

    def execute(self):
        for cmd in self.commands:
            cmd.execute()

    def undo(self):
        # Undo in reverse order
        for cmd in reversed(self.commands):
            cmd.undo()

# 4. Invoker: Manages execution, undo stacks, and redo stacks


class TextEditor:
    def __init__(self):
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute_command(self, command: Command):
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()  # Clear redo history on new action

    def undo(self):
        if not self._undo_stack:
            print("[Nothing to undo]")
            return
        cmd = self._undo_stack.pop()
        cmd.undo()
        self._redo_stack.append(cmd)

    def redo(self):
        if not self._redo_stack:
            print("[Nothing to redo]")
            return
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._undo_stack.append(cmd)


# --- Usage Example ---
doc = TextDocument()
editor = TextEditor()

# Step 1: User types "Hello World"
cmd1 = InsertTextCommand(doc, text="Hello World", position=0)
editor.execute_command(cmd1)
print(f"Current Text: '{doc.text}'")  # Hello World

# Step 2: User deletes " World"
cmd2 = DeleteTextCommand(doc, position=5, length=6)
editor.execute_command(cmd2)
print(f"After Delete: '{doc.text}'")  # Hello

# Step 3: Undo deletion
editor.undo()
print(f"After Undo:   '{doc.text}'")  # Hello World

# Step 4: Redo deletion
editor.redo()
print(f"After Redo:   '{doc.text}'")  # Hello

# Step 5: Execute a Macro (e.g., Template insertion)
macro = MacroCommand([
    InsertTextCommand(doc, text=" - Updated", position=len(doc.text)),
    InsertTextCommand(doc, text="!", position=len(doc.text) + 10)
])
editor.execute_command(macro)
print(f"After Macro:  '{doc.text}'")  # Hello - Updated!

# Step 6: Undo entire Macro in one action
editor.undo()
print(f"Undo Macro:   '{doc.text}'")  # Hello

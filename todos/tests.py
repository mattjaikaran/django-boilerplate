from django.test import TestCase
from core.models import CustomUser
from .models import Todo

# tests generated from ChatGPT based on model given


class TodoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        # Create a sample todo
        cls.todo = Todo.objects.create(
            user=cls.user,
            title="Sample Todo",
            description="This is a test todo",
            order=1,
            completed=False,
        )

    def test_todo_str(self):
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(str(todo), "Sample Todo")

    def test_todo_defaults(self):
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(todo.order, 1)
        self.assertFalse(todo.completed)

    def test_todo_creation(self):
        # Test creating a new todo
        new_todo = Todo.objects.create(
            user=self.user,
            title="New Todo",
            description="This is a new test todo",
        )
        self.assertEqual(new_todo.title, "New Todo")

    def test_todo_update(self):
        todo = Todo.objects.get(id=self.todo.id)
        todo.title = "Updated Todo"
        todo.save()
        updated_todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, "Updated Todo")

    def test_todo_deletion(self):
        todo = Todo.objects.get(id=self.todo.id)
        todo.delete()
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=self.todo.id)

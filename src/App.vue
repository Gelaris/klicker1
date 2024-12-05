<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { Todo } from "./types/todo";

const loadTodos = (): Todo[] => {
  const storedTodos = localStorage.getItem("todos");
  return storedTodos ? JSON.parse(storedTodos) : [];
};

const hideCompleted = ref(false);
const newTodo = ref("");
const todos = ref<Todo[]>([]);
const sortOption = ref("date");
const searchQuery = ref("");
const isDarkMode = ref(false);

const categories = ref(["Работа", "Личное", "Учеба"]);
const selectedCategory = ref(categories.value[0]);

onMounted(() => {
  todos.value = loadTodos();
  document.documentElement.setAttribute(
    "data-theme",
    isDarkMode.value ? "dark" : "light"
  );
});

const saveTodos = () => {
  localStorage.setItem("todos", JSON.stringify(todos.value));
};

const addTodo = () => {
  if (newTodo.value.trim()) {
    todos.value.push({
      id: Date.now(),
      text: newTodo.value.trim(),
      done: false,
      category: selectedCategory.value,
      editing: false,
    });
    newTodo.value = "";
    saveTodos();
  }
};

const removeTodo = (todo: Todo) => {
  todos.value = todos.value.filter((t) => t.id !== todo.id);
  saveTodos();
};

const editTodo = (todo: Todo) => {
  todo.editing = true;
};

const saveEditedTodo = (todo: Todo) => {
  todo.editing = false;
  saveTodos();
};

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.setAttribute(
    "data-theme",
    isDarkMode.value ? "dark" : "light"
  );
};

const clearCompleted = () => {
  todos.value = todos.value.filter((t) => !t.done);
  saveTodos();
};

const toggleAll = () => {
  const allDone = todos.value.every((t) => t.done);
  todos.value.forEach((t) => (t.done = !allDone));
  saveTodos();
};

const sortedTodos = computed(() => {
  let filtered = todos.value;
  if (hideCompleted.value) {
    filtered = filtered.filter((t) => !t.done);
  }
  if (searchQuery.value) {
    filtered = filtered.filter((t) =>
      t.text.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }
  if (sortOption.value === "alphabetical") {
    return filtered.sort((a, b) => a.text.localeCompare(b.text));
  }
  return filtered.sort((a, b) => b.id - a.id);
});
</script>

<template>
  <div class="container">
    <h1>Write your plans here</h1>

    <button @click="toggleDarkMode">
      {{ isDarkMode ? "Светлая тема" : "Темная тема" }}
    </button>

    <div class="inputholder">
      <input
        class="input"
        type="text"
        placeholder="Add Todo"
        v-model="newTodo"
      />
      <select v-model="selectedCategory">
        <option v-for="category in categories" :key="category">
          {{ category }}
        </option>
      </select>
      <button @click="addTodo">Add</button>
    </div>

    <div class="controls">
      <select v-model="sortOption">
        <option value="date">Сортировать по дате</option>
        <option value="alphabetical">Сортировать по алфавиту</option>
      </select>
      <input type="text" v-model="searchQuery" placeholder="Искать задачи" />
    </div>

    <ul>
      <li class="list" v-for="todo in sortedTodos" :key="todo.id">
        <input class="input" type="checkbox" v-model="todo.done" />
        <span :class="{ done: todo.done }" @dblclick="editTodo(todo)">
          {{ todo.text }} ({{ todo.category }})
        </span>
        <input
          v-if="todo.editing"
          v-model="todo.text"
          @blur="saveEditedTodo(todo)"
        />
        <button @click="removeTodo(todo)">Delete</button>
      </li>
    </ul>

    <button @click="toggleAll">
      {{
        todos.every((t) => t.done) ? "Снять отметку со всех" : "Завершить все"
      }}
    </button>
    <button @click="clearCompleted">Удалить выполненные</button>
    <button @click="hideCompleted = !hideCompleted">
      {{ hideCompleted ? "Показать все" : "Скрыть выполненные" }}
    </button>

    <div>
      Прогресс: {{ todos.filter((t) => t.done).length }} / {{ todos.length }}
    </div>
  </div>
</template>

<style scoped>
.container {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: "Open Sans", sans-serif;
}

h1 {
  color: #2e69f7;
  margin-bottom: 20px;
}

.done {
  text-decoration: line-through;
  color: gray;
}

.inputholder {
  display: flex;
  gap: 8px;
}

.input {
  padding: 5px;
  border-radius: 20px;
  color: #2e69f7;
  text-align: center;
}

.list {
  display: flex;
  gap: 8px;
  align-items: center;
}

.controls {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

button {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  border: none;
  color: white;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

button:hover {
  background: linear-gradient(135deg, #2575fc, #6a11cb);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.12);
}

button:active {
  transform: translateY(1px);
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2), 0 1px 2px rgba(0, 0, 0, 0.15);
}

button:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(37, 117, 252, 0.3);
}
</style>

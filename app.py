from itertools import count

from flask import Flask, redirect, render_template_string, request, url_for


app = Flask(__name__)

tasks = []
next_id = count(1)


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Task Manager</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4f1ea;
      --panel: rgba(255, 255, 255, 0.86);
      --text: #1f2937;
      --muted: #6b7280;
      --accent: #0f766e;
      --accent-soft: #d1fae5;
      --border: rgba(31, 41, 55, 0.12);
      --shadow: 0 18px 50px rgba(15, 23, 42, 0.14);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 32%),
        radial-gradient(circle at bottom right, rgba(249, 115, 22, 0.16), transparent 30%),
        var(--bg);
      min-height: 100vh;
      padding: 32px 16px;
    }

    .shell {
      width: min(760px, 100%);
      margin: 0 auto;
    }

    .hero {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: end;
      margin-bottom: 18px;
    }

    h1 {
      margin: 0;
      font-size: clamp(2rem, 5vw, 3.2rem);
      letter-spacing: -0.04em;
    }

    .subtitle {
      margin: 8px 0 0;
      color: var(--muted);
      max-width: 52ch;
      line-height: 1.5;
    }

    .badge {
      padding: 10px 14px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 700;
      white-space: nowrap;
    }

    .card {
      background: var(--panel);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .form {
      display: flex;
      gap: 12px;
      padding: 20px;
      border-bottom: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.72);
    }

    .form input {
      flex: 1;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 14px 16px;
      font: inherit;
      outline: none;
      background: white;
    }

    .form input:focus {
      border-color: rgba(15, 118, 110, 0.5);
      box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.12);
    }

    .form button,
    .action {
      border: 0;
      border-radius: 16px;
      padding: 14px 18px;
      font: inherit;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease;
    }

    .form button {
      background: var(--accent);
      color: white;
      box-shadow: 0 10px 24px rgba(15, 118, 110, 0.22);
    }

    .action {
      min-width: 92px;
      background: #111827;
      color: white;
    }

    .action.alt {
      background: #e5e7eb;
      color: #111827;
    }

    .form button:hover,
    .action:hover {
      transform: translateY(-1px);
      opacity: 0.95;
    }

    .error {
      margin: 0 20px 16px;
      padding: 12px 14px;
      border-radius: 14px;
      background: #fef2f2;
      color: #b91c1c;
      border: 1px solid #fecaca;
    }

    .list {
      list-style: none;
      padding: 10px;
      margin: 0;
    }

    .task {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 16px;
      margin: 10px;
      border-radius: 18px;
      background: white;
      border: 1px solid var(--border);
    }

    .task.done .text {
      color: var(--muted);
      text-decoration: line-through;
    }

    .text {
      margin: 0;
      font-size: 1rem;
      line-height: 1.5;
      word-break: break-word;
    }

    .meta {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .empty {
      padding: 36px 24px 40px;
      text-align: center;
      color: var(--muted);
    }

    @media (max-width: 640px) {
      .hero,
      .form,
      .task {
        flex-direction: column;
        align-items: stretch;
      }

      .badge {
        width: fit-content;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div>
        <h1>Task Manager</h1>
        <p class="subtitle">A simple Flask app to add tasks, mark them done, and remove them when you are finished.</p>
      </div>
      <div class="badge">{{ tasks|length }} tasks</div>
    </section>

    <section class="card">
      <form class="form" method="post" action="{{ url_for('home') }}">
        <input type="text" name="task" placeholder="Add a new task" autocomplete="off" autofocus>
        <button type="submit">Add Task</button>
      </form>

      {% if error %}
        <div class="error">Please type a task before adding it.</div>
      {% endif %}

      {% if tasks %}
        <ul class="list">
          {% for task in tasks %}
            <li class="task {% if task.done %}done{% endif %}">
              <p class="text">{{ task.text }}</p>
              <div class="meta">
                <a class="action alt" href="{{ url_for('toggle_task', task_id=task.id) }}">
                  {{ 'Undo' if task.done else 'Done' }}
                </a>
                <a class="action" href="{{ url_for('delete_task', task_id=task.id) }}">Delete</a>
              </div>
            </li>
          {% endfor %}
        </ul>
      {% else %}
        <div class="empty">No tasks yet. Add one above to get started.</div>
      {% endif %}
    </section>
  </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    error = False

    if request.method == "POST":
        task_text = request.form.get("task", "").strip()
        if not task_text:
            error = True
        else:
            tasks.append({"id": next(next_id), "text": task_text, "done": False})
            return redirect(url_for("home"))

    return render_template_string(PAGE, tasks=tasks, error=error)


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/ui/Header';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editTaskData, setEditTaskData] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  // Check if user is authenticated
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Check if token exists in localStorage
        const token = localStorage.getItem('access_token');
        if (!token) {
          router.push('/login');
          return;
        }

        // Load tasks
        await fetchTasks();
      } catch (err) {
        console.error('Authentication check failed:', err);
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  const fetchTasks = async () => {
    try {
      // Check if token exists in localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          return;
        }
        throw new Error('Failed to load tasks');
      }

      const tasksData = await response.json();
      setTasks(tasksData);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load tasks:', err);
      setError('Failed to load tasks');
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTask.title.trim()) return;

    try {
      // Check if token exists in localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
          completed: false
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          return;
        }
        throw new Error('Failed to add task');
      }

      const newTaskData = await response.json();
      setTasks([newTaskData, ...tasks]);
      setNewTask({ title: '', description: '' });
    } catch (err) {
      console.error('Failed to add task:', err);
      setError('Failed to add task');
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    try {
      // Check if token exists in localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          completed: !tasks.find(task => task.id === taskId)?.completed
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          return;
        }
        throw new Error('Failed to update task');
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      console.error('Failed to update task:', err);
      setError('Failed to update task');
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      // Check if token exists in localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          return;
        }
        throw new Error('Failed to delete task');
      }

      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete task');
    }
  };

  const startEditing = (task: Task) => {
    setEditingTaskId(task.id);
    setEditTaskData({
      title: task.title,
      description: task.description
    });
  };

  const updateTask = async (taskId: number, taskData: { title?: string; description?: string; completed?: boolean }) => {
    try {
      // Check if token exists in localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          return;
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update task');
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));

      // Reset edit state after successful update
      setEditingTaskId(null);
      setEditTaskData({ title: '', description: '' });
    } catch (err: any) {
      console.error('Failed to update task:', err);
      setError(err.message || 'Failed to update task');
    }
  };

  const handleEditSubmit = (taskId: number, e: React.FormEvent) => {
    e.preventDefault();
    updateTask(taskId, editTaskData);
  };

  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditTaskData({ title: '', description: '' });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center animate-fade-in-up">
          <div className="flex justify-center mb-4">
            <div className="spinner w-12 h-12" />
          </div>
          <p className="text-lg font-medium text-gray-700">Loading your tasks...</p>
          <p className="text-sm text-gray-500 mt-2">One moment please</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-purple-50">
      <Header />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Page Header */}
        <div className="mb-12 animate-fade-in-up">
          <h1 className="text-4xl font-bold mb-2">
            <span className="text-gray-900">My Tasks</span>
          </h1>
          <p className="text-gray-600 text-lg">
            {tasks.length === 0
              ? 'Start by creating your first task'
              : `You have ${tasks.length} task${tasks.length !== 1 ? 's' : ''} • ${tasks.filter((t) => t.completed).length} completed`}
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-lg flex items-start gap-3 animate-slide-down">
            <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-sm font-medium text-red-800">{error}</span>
          </div>
        )}

        {/* Add Task Form */}
        <form onSubmit={handleAddTask} className="mb-12 card glass-dark backdrop-blur-xl border border-white/20 animate-scale-in">
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label htmlFor="title" className="form-label text-gray-800">
                Task Title
              </label>
              <input
                type="text"
                id="title"
                className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors"
                placeholder="What needs to be done?"
                value={newTask.title}
                onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                required
              />
            </div>

            <div>
              <label htmlFor="description" className="form-label text-gray-800">
                Description (Optional)
              </label>
              <textarea
                id="description"
                rows={3}
                className="input-base text-gray-900 bg-white/80 hover:bg-white transition-colors resize-none"
                placeholder="Add details, notes, or reminders..."
                value={newTask.description}
                onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              />
            </div>

            <button
              type="submit"
              className="btn-primary w-full flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Task
            </button>
          </div>
        </form>

        {/* Tasks List */}
        <div className="space-y-4">
          {tasks.length === 0 ? (
            <div className="card glass-dark backdrop-blur-xl border border-white/20 text-center py-16 animate-fade-in-up">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 rounded-full bg-accent-primary/10 flex items-center justify-center">
                  <svg className="w-8 h-8 text-accent-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
              </div>
              <p className="text-lg font-medium text-gray-700 mb-2">No tasks yet</p>
              <p className="text-gray-500 mb-6">Create your first task to get started</p>
              <button
                onClick={() => document.getElementById('title')?.focus()}
                className="btn-primary inline-flex"
              >
                Create Task
              </button>
            </div>
          ) : (
            tasks.map((task, index) => (
              <div
                key={task.id}
                className="card glass-dark backdrop-blur-xl border border-white/20 hover:shadow-glow-lg transition-all duration-300 animate-slide-up"
                style={{animationDelay: `${index * 50}ms`}}
              >
                {editingTaskId === task.id ? (
                  // Edit Mode
                  <form onSubmit={(e) => handleEditSubmit(task.id, e)} className="space-y-4">
                    <div className="flex items-start gap-4">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => toggleTaskCompletion(task.id)}
                        className="w-5 h-5 text-accent-primary border-gray-300 rounded-lg cursor-pointer mt-1 accent-accent-primary"
                      />
                      <div className="flex-1 space-y-3">
                        <input
                          type="text"
                          value={editTaskData.title}
                          onChange={(e) => setEditTaskData({...editTaskData, title: e.target.value})}
                          className="input-base text-gray-900 bg-white/80"
                          placeholder="Task title"
                          required
                        />
                        <textarea
                          value={editTaskData.description}
                          onChange={(e) => setEditTaskData({...editTaskData, description: e.target.value})}
                          className="input-base text-gray-900 bg-white/80 resize-none"
                          placeholder="Task description"
                          rows={2}
                        />
                        <div className="flex gap-2">
                          <button
                            type="submit"
                            className="btn-primary text-sm flex items-center gap-2"
                          >
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" />
                            </svg>
                            Save
                          </button>
                          <button
                            type="button"
                            onClick={cancelEditing}
                            className="btn-outline text-sm flex items-center gap-2"
                          >
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                            Cancel
                          </button>
                        </div>
                      </div>
                    </div>
                  </form>
                ) : (
                  // Display Mode
                  <div className="flex items-start gap-4">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => toggleTaskCompletion(task.id)}
                      className="w-5 h-5 text-accent-primary border-gray-300 rounded-lg cursor-pointer mt-1 accent-accent-primary"
                    />

                    <div className="flex-1">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <p className={`text-base font-semibold transition-all duration-300 ${
                            task.completed
                              ? 'line-through text-gray-400'
                              : 'text-gray-900'
                          }`}>
                            {task.title}
                          </p>
                          {task.description && (
                            <p className={`text-sm mt-1 transition-all duration-300 ${
                              task.completed
                                ? 'line-through text-gray-400'
                                : 'text-gray-600'
                            }`}>
                              {task.description}
                            </p>
                          )}
                        </div>

                        <div className="flex items-center gap-2 flex-shrink-0">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold transition-all duration-300 ${
                            task.completed
                              ? 'badge-success'
                              : 'badge-warning'
                          }`}>
                            {task.completed ? 'Completed' : 'Pending'}
                          </span>

                          <button
                            onClick={() => startEditing(task)}
                            className="p-2 hover:bg-blue-100/50 rounded-lg transition-colors text-blue-600 hover:text-blue-700"
                            title="Edit task"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                          </button>

                          <button
                            onClick={() => deleteTask(task.id)}
                            className="p-2 hover:bg-red-100/50 rounded-lg transition-colors text-red-600 hover:text-red-700"
                            title="Delete task"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
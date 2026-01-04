// This is a server component that fetches tasks from the backend
// In a real implementation, this would be a server component that fetches data
// For now, we'll implement it as a client component since we don't have a backend yet

'use client';

import { useState } from 'react';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function TaskList({ initialTasks }: { initialTasks: Task[] }) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);

  const toggleTaskCompletion = async (id: number) => {
    try {
      // TODO: Replace with actual API call to backend
      // const token = localStorage.getItem('token');
      // await fetch(`/api/tasks/${id}/complete`, {
      //   method: 'PATCH',
      //   headers: {
      //     'Authorization': `Bearer ${token}`
      //   }
      // });

      // For now, update local state
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      ));
    } catch (err) {
      console.error('Failed to update task', err);
    }
  };

  const deleteTask = async (id: number) => {
    try {
      // TODO: Replace with actual API call to backend
      // const token = localStorage.getItem('token');
      // await fetch(`/api/tasks/${id}`, {
      //   method: 'DELETE',
      //   headers: {
      //     'Authorization': `Bearer ${token}`
      //   }
      // });

      // For now, update local state
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      console.error('Failed to delete task', err);
    }
  };

  return (
    <div className="bg-white shadow overflow-hidden rounded-lg">
      <ul className="divide-y divide-gray-200">
        {tasks.length === 0 ? (
          <li className="px-4 py-8 text-center">
            <p className="text-gray-500">No tasks yet. Add your first task above!</p>
          </li>
        ) : (
          tasks.map((task) => (
            <li key={task.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => toggleTaskCompletion(task.id)}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <div className="ml-3">
                    <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {task.title}
                    </p>
                    {task.description && (
                      <p className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-500'}`}>
                        {task.description}
                      </p>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${task.completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {task.completed ? 'Completed' : 'Pending'}
                  </span>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
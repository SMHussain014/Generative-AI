'use server'

import { revalidatePath } from "next/cache"

// add todos
export default async function add_todos(
    state: { status: string, message: string }, formData: FormData
) {
    const new_todo = formData.get('add_task') as string
    // add form validation through Zod
    try {
        const response = await fetch('http://localhost:8000/todos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: new_todo, content: new_todo })
        })
        revalidatePath('/todos')
        return {status: 'success', message: 'Todo added successfully'}
    }
    catch (error) {
        return {status: 'error', message: 'Opps! something went wrong'}
    }
}
// status change for todos
export async function status_change(
    id: number, title: string, content: string, is_completed: boolean
) {
    // add form validation through Zod
    try {
        const response = await fetch(`http://localhost:8000/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
            { id: id, title: title, content: content, is_completed: !is_completed })
        })
        const resp = await response.json()
        revalidatePath('/todos')
        return {status: 'success', message: 'Status changed successfully'}
    }
    catch (error) {
        return {status: 'error', message: 'Opps! something went wrong'}
    }
}
// edit todos
export async function edit_todos(
    state: { status: string, message: string }, 
    { id, title, content, is_completed }: 
    { id: number, title: string, content: string, is_completed: boolean}
) {
    // add form validation through Zod
    try {
        const response = await fetch(`http://localhost:8000/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
            { id: id, title: title, content: content, is_completed: is_completed })
        })
        revalidatePath('/todos')
        return {status: 'success', message: 'Todo edited successfully'}
    }
    catch (error) {
        return {status: 'error', message: 'Opps! something went wrong'}
    }
}
// status change for todos
export async function del_todos(id: number) {
    // add form validation through Zod
    try {
        const response = await fetch(`http://localhost:8000/todos/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        const resp = await response.json()
        revalidatePath('/todos')
        return {status: 'success', message: 'Todo deleted successfully'}
    }
    catch (error) {
        return {status: 'error', message: 'Opps! something went wrong'}
    }
}
'use client'

import { Todo } from "@/lib/types";
import { useFormState } from "react-dom"
import { edit_todos } from "@/actions/actions";
import SubmitButton from "@/components/SubmitButton";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

export default function EditTask({task}: {task: Todo}) {
    const [value1, setValue1] = useState(task.title)
    const [value2, setValue2] = useState(task.content)
    const [state, formAction] = useFormState(edit_todos, { status: "", message: "" })
    const { status, message } = state
    const handleChange1 = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue1(e.target.value)
    }
    const handleChange2 = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue2(e.target.value)
    }
    const handleSubmit = (formData: FormData) => {
        const id: number = task.id
        const title: string = formData.get('edit_task') as string
        const content: string = formData.get('edit_content') as string
        const is_completed: boolean = task.is_completed
        formAction({ id, title, content, is_completed })
    }
    useEffect(() => {
        if (status === "success") {
            toast.success(message)
        }
        else if (status === "error") {
            toast.error(message)
        }
    }, [state])
    return (
        <form action = {handleSubmit} 
        className="flex flex-col justify-between items-center gap-x-3">
            <input 
            onChange = {handleChange1}
            type="text"
            minLength={8}
            maxLength={54}
            name="edit_task"
            value={value1}
            required 
            className="w-full px-2 py-1 border border-gray-100 rounded-md mb-4"
            />
            <input 
            onChange = {handleChange2}
            type="text"
            minLength={8}
            maxLength={54}
            name="edit_content"
            value={value2}
            required 
            className="w-full px-2 py-1 border border-gray-100 rounded-md mb-4"
            />
            <SubmitButton />
        </form>
    )
}
'use client'

import { useFormState } from "react-dom"
import add_todos from "@/actions/actions"
import { useEffect, useRef } from "react"
import toast from "react-hot-toast"
import SubmitButton from "@/components/SubmitButton"

export default function AddTask() {
    const ref = useRef<HTMLFormElement>(null)
    const [state, formAction] = useFormState(add_todos, { status: "", message: "" })
    const { status, message } = state
    useEffect(() => {
        if (status === "success") {
            ref.current?.reset()
            toast.success(message)
        }
        else if (status === "error") {
            toast.error(message)
        }
    }, [state])
    return (
        <form ref={ref} action={formAction}
            className="flex flex-col justify-between items-center gap-x-3">
            <input
                type="text"
                placeholder="Add Task Here"
                minLength={8}
                maxLength={54}
                name="add_task"
                required
                className="w-full px-2 py-1 border border-gray-100 rounded-md mb-4"
            />
            <input
                type="text"
                placeholder="Add Content Here"
                minLength={8}
                maxLength={54}
                name="add_content"
                required
                className="w-full px-2 py-1 border border-gray-100 rounded-md mb-4"
            />
            <SubmitButton />
        </form>
    )
}

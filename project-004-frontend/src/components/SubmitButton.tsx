import { useFormStatus } from "react-dom"

export default function SubmitButton() {
    const { pending } = useFormStatus()
    return (
        <button className="px-2 py-1 bg-teal-600 text-white rounded-md"
        disabled={pending}
        >
            {
                pending ? "Saving ..." : "Save"
            }
        </button>
    )
}

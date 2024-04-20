import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import AddTask from "@/components/AddTask"
import EditTask from "@/components/EditTask"
import { Todo } from "@/lib/types"

export function Modal(
    { children, title, add, edit, task }:
    { children: React.ReactNode, title: string, add?: boolean, edit?: boolean, task: Todo }
) {
    return (
        <Dialog>
            <DialogTrigger asChild>
                {children}
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>{title}</DialogTitle>
                </DialogHeader>
                {add && <AddTask />}
                {edit && <EditTask task={task} />}
            </DialogContent>
        </Dialog>
    )
}

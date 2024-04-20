'use client'

import { Todo } from "@/lib/types";
import { CiSquareCheck } from "react-icons/ci";
import { FiEdit, FiTrash2 } from "react-icons/fi";
import { ToolTip } from "@/components/ToolTip";
import { Modal } from "@/components/Modal";
import { del_todos, status_change } from "@/actions/actions";
import toast from "react-hot-toast";

export default function Tasks({ task }: { task: Todo }) {
  const handleStatus = async () => {
    const response = await status_change(
      task.id,
      task.title,
      task.content,
      task.is_completed
    )
    if (response.status === "success") {
      toast.success(response.message)
    }
    else if (response.status === "error") {
      toast.error(response.message)
    }
  }
  const handleDelete = async () => {
    const response = await del_todos(task.id)
    if (response.status === "success") {
      toast.success(response.message)
    }
    else if (response.status === "error") {
      toast.error(response.message)
    }
  }
  return (
    <tr className="flex justify-between items-center border-b border-gray-300 p-2">
      <td>{task.title}</td>
      <td className="flex gap-x-2">
        <button onClick={handleStatus}>
          <ToolTip tool_tip_content="Mark as completed">
            <CiSquareCheck size={28}
              className={`${task.is_completed ? "text-green-500" : "text-gray-400"}`}
            />
          </ToolTip>
        </button>

        <ToolTip tool_tip_content="Add new Task">
          <Modal title="Edit Task" edit={true} task={task}>
            <FiEdit size={24} className="text-blue-500" />
          </Modal>
        </ToolTip>

        <button onClick={handleDelete}>
          <ToolTip tool_tip_content="Delete a Todo">
            <FiTrash2 size={24} className="text-red-500" />
          </ToolTip>
        </button>

      </td>
    </tr>
  )
}

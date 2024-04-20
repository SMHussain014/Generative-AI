import { Modal } from "@/components/Modal";
import TodoTable from "@/components/TodoTable";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="max-w-5xl mx-auto mt-8">
      {/* Add Task */}
      <section>
        <Modal title="Add New Task" add={true}>
          <Button variant="default"
            className="w-full px-2 py-1 bg-teal-600 text-white text-lg uppercase">
            Add Task +
          </Button>
        </Modal>
      </section>
      {/* Add Task Table */}
      <section className="mt-4">
        <TodoTable />
      </section>
    </main>
  );
}

import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export function ToolTip({tool_tip_content, children}: {tool_tip_content: string, children: React.ReactNode}) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          {children}
        </TooltipTrigger>
        <TooltipContent>
          <p>{tool_tip_content}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

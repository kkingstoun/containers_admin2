import { Button } from "@/registry/new-york-v4/ui/button"
import { Separator } from "@/registry/new-york-v4/ui/separator"
import { SidebarTrigger } from "@/registry/new-york-v4/ui/sidebar"
import { ModeToggle } from "@/app/dashboard/components/mode-toggle"
import { ThemeSelector } from "@/app/dashboard/components/theme-selector"

export function SiteHeader() {
  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1" />
        <Separator
          orientation="vertical"
          className="mx-2 data-[orientation=vertical]:h-4"
        />
        <h1 className="text-base font-medium">PCSS containers v 0.2</h1>
        <div className="ml-auto flex items-center gap-2">
          <ModeToggle />
          {/* <ThemeSelector /> */}
        </div>
      </div>
    </header>
  )
}

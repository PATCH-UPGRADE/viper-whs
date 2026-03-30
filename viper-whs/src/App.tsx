import { Button } from "./components/ui/button"

function App() {
  return (
    <>
      <div className="flex flex-col gap-4">
        <h1 className="font-bold">Whole Hospital Simulator</h1>

        <div className="flex flex-col gap-4">
          <h2 className="font-bold">Console Logs</h2>
          <textarea readOnly rows={16} cols={16} className="font-mono bg-black text-white p-4 border-gray-800 focus:outline-none">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus et nulla eu massa posuere vehicula. Donec venenatis sollicitudin tellus nec mattis. Vivamus et sem laoreet, pellentesque purus vel, maximus arcu. Morbi odio felis, imperdiet sit amet convallis in, faucibus vitae nisl. Donec mollis tortor a diam posuere molestie. Praesent non dolor quis diam ultricies ultrices aliquet ac lacus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vivamus maximus ex sed augue faucibus, vitae condimentum urna iaculis. Sed rutrum scelerisque tortor, nec ornare turpis rhoncus sit amet. Vivamus scelerisque, justo ac porta molestie, enim magna dignissim metus, sed varius nibh eros vitae mi. Suspendisse auctor velit id posuere fermentum. Ut tempor tortor dui, non eleifend diam mollis maximus. 
          </textarea>
        </div>
        <div>
          <Button>Start</Button>
          <Button>Stop</Button>
          <Button variant="destructive">Delete</Button>
        </div>
      </div>
    </>
  )
}

export default App

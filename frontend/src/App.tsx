import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Layout } from "./components/Layout";
import { HistoryPage } from "./pages/HistoryPage";
import { HomePage } from "./pages/HomePage";
import { ResultsPage } from "./pages/ResultsPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "tasks/:taskId/edit", element: <HomePage /> },
      { path: "history", element: <HistoryPage /> },
      { path: "results/:runId", element: <ResultsPage /> },
      { path: "results/compare/:taskId", element: <ResultsPage /> },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}

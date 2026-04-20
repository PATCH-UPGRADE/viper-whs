import { useQuery } from "@tanstack/react-query";
import { getTopologies } from "./hooks";
import type { TopologiesResponse } from "./types";

export const TopologiesContainer = () => {
  const {
    data: topologies,
    isPending,
    isError,
    _error,
  } = useQuery({
    queryKey: ["topologies"],
    queryFn: getTopologies,
  });

  if (isPending) {
    return <TopologiesLoading />;
  }

  if (isError) {
    return <TopologiesError />;
  }

  return <TopologiesList topologies={topologies} />;
};

const TopologiesLoading = () => {
  return <div>Topologies loading...</div>;
};

const TopologiesError = () => {
  return <div>An error occured while loading topologies!</div>;
};

interface TopologiesListI {
  topologies: TopologiesResponse;
}

const TopologiesList = ({ topologies }: TopologiesListI) => {
  return (
    <div>
      {topologies.map((topo, index) => (
        <div key={index}>{topo.name}</div>
      ))}
    </div>
  );
};

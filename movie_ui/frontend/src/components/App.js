import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

const App = () => (
  <DataProvider endpoint="movie/?order_by=release_date&direction=asc"
                render={data => <Table data={data} />} />
);

const wrapper = document.getElementById("movie");

wrapper ? ReactDOM.render(<App />, wrapper) : null;

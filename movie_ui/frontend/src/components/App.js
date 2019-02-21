import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

const App = () => (
  <DataProvider endpoint="api/movie/"
                render={data => <Table data={data} />} />
);

const wrapper = document.getElementById("movie");

wrapper ? ReactDOM.render(<App />, wrapper) : null;

import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";


const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        Showing <strong>{data.length} items</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            {Object.entries(data[0]).map(el => <th key={key(el)}>{el[0]}</th>)}
          </tr>
        </thead>
        <tbody>
          {
              data.map(el => (
                <tr key={el.id}>
                    <td>{el.title}</td>
                    <td>{el.release_date}</td>
                    <td>{el.imdb_id}</td>
                    <td>{el.imdb_rating}</td>
                    <td>
                        <a href={el.imdb_movie_url}>{el.imdb_movie_url}</a>
                    </td>
                    <td>
                        <a href={el.trailer}>{el.trailer}</a>
                    </td>
                </tr>
              ))
          }
        </tbody>
      </table>
    </div>
  );

Table.propTypes = {
  data: PropTypes.array.isRequired
};

export default Table;

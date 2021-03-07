// Step #1, import Statements
import React from "react";
import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import {
  PagingInfo,
  ResultsPerPage,
  Paging,
  Facet,
  SearchProvider,
  Results,
  SearchBox,
  Sorting
} from "@elastic/react-search-ui";
// Step #2, The Connector
const connector = new AppSearchAPIConnector({
  searchKey: "search-25c4zpqjindf3z9pnjpjm76p",
  engineName: "sampleengine",
  // endpointBase: "https://1fbea0f61f3144fd9c130161f7f707bc.ent-search.us-central1.gcp.cloud.es.io"
  endpointBase: "https://1fbea0f61f3144fd9c130161f7f707bc.ent-search.us-central1.gcp.cloud.es.io/"
});
// Step #3: Configuration Options
const configurationOptions = {
  apiConnector: connector,
  searchQuery: {
    search_fields: {
      // 1. Search by name of video game.
      recipe_title : {},
      special_equipment: {}
    },
    result_fields: {
      recipe_title:{
        snippet: {
          size: 100, // Limit the snippet to 75 characters.
          fallback: true // Fallback to a "raw" result.
        }
      },
      special_equipment:{
        snippet: {
          size: 100, // Limit the snippet to 75 characters.
          fallback: true // Fallback to a "raw" result.
        }
      },
      direction:{
        snippet: {
          size: 100, // Limit the snippet to 75 characters.
          fallback: true // Fallback to a "raw" result.
        }
      },
      recipe_link:{
        raw: {}
      },
      total_time:{
        raw: {}
      },
      active_time:{
        raw: {}
      },
      ingredients:{
        raw: {}
      }
    }, ///end of result fields
    facets: {
      total_time:{
        type:"range",
        ranges:[
          {from: 0, to: 31, name: "0~30 min"},
          {from: 31, to: 61, name: "31 min ~ 1 hour"},
          {from: 61, to: 91, name: "1 hour ~ 1.5 hour"},
          {from: 91, to: 121, name: "1.5 hour ~ 2 hour"},
          {from: 121, to: 181, name: "2 hour ~ 3 hour"},
          {from: 180, to: 241, name: "3 hour ~ 4 hour"},
          {from: 240, to: 10000, name: "more than 4 hour"}
        ]
      }
    }
  }

};
// Step #4, SearchProvider: The Finishing Touches.
export default function App() {
  return (
    <SearchProvider config={configurationOptions}>
      <div className="App">
      <Layout
  // header={<SearchBox />}
  header={<SearchBox autocompleteSuggestions={true} />}
  bodyContent={<Results titleField="name" urlField="image_url" />}
  sideContent={
    <div>
      <Sorting
        label={"Sort by"}
        sortOptions={[
          {
            name: "Relevance",
            value: "",
            direction: ""
          },
          {
            name: "recipe title",
            value: "recipe_title",
            direction: "asc"
          }
          ,
          {
            name: "total_time",
            value: "total_time",
            direction: "asc" // work now 
          },
          {
            name: "active_time",
            value: "active_time",
            direction: "asc" // work now 
          }
        ]}
      />
      <Facet field="total_time" label="Total Time" />
    
    </div>
  }
  bodyHeader={
    <>
      <PagingInfo />
      <ResultsPerPage />
    </>
  }
  bodyFooter={<Paging />}
/>
      </div>
    </SearchProvider>
  );
}
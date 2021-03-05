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
  engineName: "recipes",
  endpointBase: "https://1fbea0f61f3144fd9c130161f7f707bc.ent-search.us-central1.gcp.cloud.es.io"
});
// Step #3: Configuration Options
const configurationOptions = {
  apiConnector: connector
  // Let's fill this in together.
};
// Step #4, SearchProvider: The Finishing Touches.
export default function App() {
  return (
    <SearchProvider config={configurationOptions}>
      <div className="App">
      <Layout
  header={<SearchBox />}
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
            name: "Name",
            value: "name",
            direction: "asc"
          }
        ]}
      />
      {/* <Facet field="user_score" label="User Score" />
      <Facet field="critic_score" label="Critic Score" />
      <Facet field="genre" label="Genre" />
      <Facet field="publisher" label="Publisher" isFilterable={true} />
      <Facet field="platform" label="Platform" /> */}
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
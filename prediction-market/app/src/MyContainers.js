import MyComponent from "./MyComponent";
import { drizzleConnect } from "@drizzle/react-plugin";
import About from './components/About';

const mapStateToProps = state => {
  return {
    accounts: state.accounts,
    PredictionMarket: state.contracts.PredictionMarket,
    drizzleStatus: state.drizzleStatus,
  };
};

export const MainContainer = drizzleConnect(MyComponent, mapStateToProps);
export const AboutContainer = drizzleConnect(About, mapStateToProps);

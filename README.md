# TSA Checkpoint Throughput and Weather Project

## Project Description
This project analyzes data from the TSA's public checkpoint throughput figures and Weather API. The data used for this project was retrieved from the [TSA FOIA Reading Room](https://www.tsa.gov/foia/readingroom).

## Data Dictionary

The data includes passenger count per hour for different airports and their checkpoints.

| Column Name             | Description                                                  | Data Type |
| ----------------------- | ------------------------------------------------------------ | --------- |
| Date                    | Date of data collection                                      | Date      |
| Hour of Day             | Hour of the day (24 hour format)                             | String    |
| Airport                 | Code of the airport                                          | String    |
| City                    | City where the airport is located                            | String    |
| State                   | State where the airport is located                           | String    |
| Checkpoint              | Specific checkpoint at the airport                           | String    |
| Total Pax + KCM PAX     | Total passenger count including Known Crewmember (KCM) passengers at each checkpoint for the given hour | Integer   |

Note that all dates are formatted as 'mm/dd/yyyy'.


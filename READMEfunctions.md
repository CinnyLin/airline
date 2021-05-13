# app.py

## Public Information
1. **search flight information**: using dates, departure cities/airports, airlines, or prices
    1. `app.py`: searchFlight()
    2. `templates`: index.html, publicSearchFlights.html
2. **search flight statuses**: based on airline name, flight number, or ticket id
    1. `app.py`: searchFlightStatus()
    2. `templates`: index.html, publicSearchFlightStatus.html

## Common User Functions
Three types of users: customers, booking agents, airline staffs
1. **register**: users can sign up as either types of users; quotation marks in input would be escaped
    1. `app.py`: registerAgent(), registerCustomer(), registerStaff(), registerAgentAuth(), registerCustomerAuth(), registerStaffAuth()
    2. `templates`: registerAgent.html, registerCustomer.html, registerStaff.html

2. **login**: when users login they would not have access to pages of other users
    1. `app.py`: login(), loginAgent(), loginCustomer(), loginStaff(), loginAgentAuth(), loginCustomerAuth(), loginStaffAuth()
    2. `templates`: login.html, loginAgent.html, loginCustomer.html, loginStaff.html

3. **delete account**: users would be required to authenticate their email and password before deleting their account; with SQL ON DELETE CASCADE, their personal data would be deleted but anonymous purchase history would be kept
    1. `app.py`: deleteAccountAgent(), deleteAccountCustomer(), deleteAccountStaff(), deleteAccountAgentAuth(), deleteAccountCustomerAuth(), deleteAccountStaffAuth()
    2. `templates`: deleteAgent.html, deleteCustomer.html, deleteStaff.html

4. **reset password**: users would be required to authenticate their email and password before resetting their password, and would be redirected to login again
    1. `app.py`: resetAgent(), resetCustomer(), resetStaff()
    2. `templates`: resetAgent.html, resetCustomer.html, resetStaff.html

5. **logout**: users would be logged out
    1. `app.py`: logout()

## Customer Exclusive Functions
1. **view flights**: Platform provides various ways for the user to see flights information which they purchased.
    1. `customerViewTickets()` shows upcoming flights as default.

2. **search and purchase flights**: Customer searches for upcoming flights based on city/airport, date etc. and purchase tickets for this flight.
    1. `customerSearchPurchase()`: renders the search/purchase front page
    2. `customerSearchFlights()`: sends search request to back-end and render search results to front-end
    3. `customerPurchaseTicket()`: pass search request to purchase function and pass to front-end

3. **track spendings**: Customer can see total amount of money spent and montly spendings breakdown for a selected period of time.
    1. `customerTrackSpending()`: default view shows total amount of money spent in the past year and a bar chart showing month-wise money spending for the last 6 months.

## Booking Agent Exclusive Functions
1. **view flights**: Agent can see the flights information that they purchased on behalf of their customers. 
    1. `agentViewTicket()`: default shows upcoming flights.

2. **search and purchase flights**: Agent searches for upcoming flights based on city/airport, date etc. and purchase tickets for this flight on behalf of customers.
    1. `agentSearchPurchase()`: renders the search/purchase front page
    2. `agentSearchFlights()`: sends search request to back-end and render search results to front-end
    3. `agentPurchaseTicket()`: pass search request to purchase function and pass to front-end; agent would have to enter the customer email to purchase on their behalf

3. **view commission**: Agent can see total amount of commission received, average commission per ticket, and number of tickets booked for a selected period of time.
    1. `agentCommission()`: default view shows the results from the past month.

## Airline Staff Exclusive Functions
1. **view flights**: Staff can see the flights information operated by their airline.
    1. `staffViewFlights()`: default shows all upcoming flights for their airline in the next 30 days.

2. **edit flight data**: Staff can change flight information within their airline.
    1. `editFlightData()`: renders the front page where staffs can do all the edit data operations
    2. `editFlightStatus()`: allows staff to change flight status (from upcoming to in progress, in progress to delayed etc).
    3. `addFlight()`: staff can create a new flight by providing flight number, airplane id, departure/arrival time and airport, flight price,  flight status, and seats (i.e. number of tickets left). 
    **Note1**: Here it would check if the "number of tickets left (`flight.num_tickets_left`)" is less than or equal to "the number of seats of the airplane" (`airplane.seats`).
    **Note2**: `num_tickets_left` is a new column we added in the `flight` table in order to check if there is still tickets left when customers/agents make their flight purchases.
    4. `addAirplane()`: staff can create a new airplane for their airline by providing airplane id and number of seats that airplane has.
    5. `addAirport()`: staff can create a new airport by providing the airport name and airport city.
    6. Each function checks if the added information is already in our database system. It returns appropriate messages after an edit, such as an error message saying that the airport already exists.
    7. The application prevents unauthorizaed users from doing these actions by checking the session of the user in each operation (`if session.get('username')`) and separating the routing path of all users (`/staff/[editFlightDataOperation]`)
    

3. **booking agent**: Staff can see top 5 booking agents based on the number of tickets they sold and the amount of commission they received.
    1. `staffTopAgent()`: default shows number of tickets sold for the past month, and amount of commission received the last year.

4. **customers**: Staff can see different information about customers of their airline.
    1. `staffTopCustomer()`: shows the most frequent customer within the last year.
    2. `staffCustomerFlight()`: shows a list of flights in their airline that this customer has taken.
    3. `staffFlightCustomer()`: shows a list of customers of this flight in their airline.

5. **numbers**: Staff can see relevant numbers that help them understand the business of their airline.
    1. `staffTicketReport()`: renders the ticket front page.
    2. `staffTicket()`: shows the total amounts of ticket sold and monthly tickets sold breakdown in a bar chart from on a selected period.
    3. `staffEarningsReport()`: shows pie charts of total revenue earned from direct sales (customer directly buying from airline) and indirect sales (customers buying through agent) in the past month and past year.
    4. `staffTopDestinations()`: shows the top 3 most popular destination for the past 3 months and past year.
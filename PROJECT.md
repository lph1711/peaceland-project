# SPARK PROJECT 2023

## Authors

- Youssef BOUAFA DINIA (youssef.bouafar-dinia)

- Yassin BOUHASSOUN  (yassin.bouhassoun)

- Phu Hien LE (phu-hien.le)

- Luu Hoang Long VO (luu-hoang-long.vo)

***

## Response

### Question 1

1. What technical/business constraints should the data storage component of the program architecture meet to fulfill the requirement described by the customer in paragraph «Statistics» ?  
    A.  Technical Constraint :
    - Large data storage to be able to store >200Gb of daily reports from peacewatchers

    - Since the peacemakers still do not know what kind of statistics they want to address, we need to categorize the data for faster extraction.
      - We do that by implementing a data warehouse designed specifically for the use of BI and Analytics

    - Since only less than 1% of the data contains alert, we need to implement an efficient search algorithm
      - Search algorithms that can extract the alert containing report (faster) with certain name as parameters

    - Redundancy—distributed storage systems can store more than one copy of the same data, for high availability, backup, and disaster recovery purposes.
      - Maybe of having to implement a distributed storage system as the main database

    - The system must have scalability, peacemaker officers may add more waves of peacewatcher in the future.
      - Having multiple stream processors to handle each specific task will help with scalability and efficiency

    B. Business Constraint :
    - 1 day to categorize everything

    - Cost—distributed storage makes it possible to use cheaper, commodity hardware to store large volumes of data at low cost (thanks to the horizontal scaling vs the vertical scaling that is expensive)

2. What kind of component(s) (listed in the lecture) will the architecture need?
    - Data storage: NoSQL, Availability and Partition Tolerance  
      - Fast access time will help with Availability

    - Examples of NoSQL databases:
      - MongoDB (most popular)
      - Redis
      - RavenDB

    - Distributed storage system will make sure the data will be accessible even when some of the partitions fail. (No loss of data)

***

### Question 2

1. What business constraint should the architecture meet to fulfill the requirement described in the paragraph «Alert»?
    - Must distribute the alert to the peacekeeper as fast as possible, preferably to the nearest possible peacekeeper based on the peacewatcher location report.

    - Find a scalable notification server with good economy of scales (stream consumer) to handle the distribution of bad peace score to the peacekeepers as fast as possible. (Google Firebase, Amazon SNS)

    - An efficient streaming processor component must be used to find the alert as fast as possible, since only less than 1% of the data in the storage are alerts. These kinds of processors will have excessive costs for the extra processing.

2. Which components to use?
    - Stream Broker: We need functionalities to handle the data. We think that kafka streaming or spark streaming are the references.

    - Notification Service:  
      - Google Firebase, Amazon SNS:
          1. Easy to customize to the clients’ need
          2. No physical hardware to maintain
          3. Adaptive and scalable as the amount of alert grows
          4. Data is passed through to a third party, more prone to security breaches
      - Self-hosted server:
          1. Since the service is for the government, self-hosted will make sure the data is more secure and is not stored on a third party
          2. Harder to maintain with required a physical space as well as a maintainer as a staff

    - Stream processing: near real time (we need the pacemakers to get the alert fast), and process a small amount of data, which is the case with all the small reports being sent.

    - Batch processing: Did not choose batch processing because it processes data periodically, therefore we do not get real time data which is relevant since we want the peacemakers to get alerted by the drones fast.

***

### Question 3

What mistake(s) from Peaceland can explain the failed attempt?

- The POC was ‘thrown’ into production. The POC may not be extensively researched and maybe needs a modification before it can be put into production. The problem arises from the lack of experience and consideration from the data scientist team on system architecture design aspect. A failed POC on production is an expensive failure, may cost the PeaceLand government a lot of money.

- The data scientists chose SQL as Data Storage which does not scale well with bigger data. They should have chosen a NoSQL database to implement. NoSQL databases can be scaled well with bigger data, and they can handle high speed and volume data.

- The data scientist team may have used vertical scaling instead of horizontal scaling. Vertical scaling is limited to the capacity of one machine, scaling beyond that capacity can involve downtime and has an upper hard limit. On the other hand, horizontal scaling adds more machines to the process, allowing the team to scale with less downtime.

- They chose an inappropriate CAP theorem for each data storage component. The client’s need to save every peacewatcher data isn’t satisfied, but in this case, we do have to make sacrifice so that we don’t go over budget and keep core functionality. The best CAP choice for the data storage components in this case should be Availability and Partition Tolerance.
  - Partition Tolerance so if the systems break it can still work thanks to backup stream processor 1 and the backup connection. Only do it for stream processor 1 and not 2 because of the budget and the 1st   processor is way more important. (Importance sending alert > importance of doing analysis).
  - Availability to make sure that the peacekeepers always get the alerts and the reports, it does not guarantee that it is the latest data, but it is not necessary need it.  
  - Did not choose Consistency because the data on the reports will not be modified, therefore we do not need to constantly keep the data updated. Also, we do not need the data scientist to access the latest data always, so consistency is not a priority in this designed system

- Lack of skill, efficiency and incompetent recruitment of data scientists.​

***

### Question 4

Peaceland has forgotten some technical information in the report sent by the drone. In the future, this information could help Peaceland make its peacewatchers much more efficient. Which information?

- Surrounding peacewatchers id in the same area:
  - Pros:
    - To make sure that the alert that is being sent is going to be notified just once if the peacewatcher that is in the same area has already done it  
    - Save resources on the stream processor for a quicker process of flagging the report.
  - Cons:
    - All extra information means extra data that is being sent, processed, and stored. That leads to more resources needing to be used to store the data and process it.

- Checking if the peacekeeper id is occupied (list of available peacekeepers in the area for the Stream Processor 1 to choose):
  - Pros:
    - To make sure that the alert has been sent to an available peacekeeper and not to an occupied one who is processing another alert.
    - The citizen who has a negative peacescore can be detected more quickly.
  - Cons:
    - All extra information means extra data that is being sent, processed, and stored. That leads to more resources needing to be used to store the data and process it. Slow down report processing time.
    - Affect the time the alert is being sent (latency)

- We can add to the drone information suspicious actions of the citizens:  
  - Pros:
    - The words heard by the citizens are not enough. The citizens can be silent and have a peacescore negative. Therefore, we need to also see if they are having suspicious actions or not.  
  - Cons:  
    - All extra information means extra data that is being sent, processed, and stored. That leads to more resources needing to be used to store the data and process it. Slow down report processing time
    - Affect time the alert is being sent (latency)

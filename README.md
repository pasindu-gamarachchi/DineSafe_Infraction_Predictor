# DineSafe Infraction Predictor
Machine Learning Algorithms predict the outcomes of health inspections for businesses in Toronto.

# Abstract

  Health code violation can result in fines exceeding $1000, and can damage the image of an establishment. 
Information regarding violations are easily available to potential customers through social media and local blogs such as [blogTO](https://www.blogto.com/eat_drink/2018/09/toronto-dinesafe-tim-hortons-wing-machine-3-brewers-big-smoke-burger/). 
The DineSafe Predictive Model uses Yelp reviews, and relevant business data to predict the outcome of an establishment’s 
next inspection. Using the prediction, establishments can make the necessary adjustments to prevent infractions. Firstly, the model 
predicts whether a violation will occur for a given inspection, then an independent model predicts the type of prediction. The results
of the model are shown below.

<p float = "left">
  <img src="Results/Violations.png" width = 400 >
  <img src="Results/Violation_Severity.png" width = 400 >
</p>


# Introduction

The goals of the project are to firstly, predict whether a given health inspection will result in a violation, which results in a binary prediction of a violation or a pass. A health code violation has three levels of severity, 'minor,' 'significant,' and 'crucial.' An independent model was built to predict the type of violation resulting from a health inspection; this prediction could also result in a ‘pass.’ This results in a four-class prediction problem. 
‘Minor’ violations are defined as ‘Infractions that present a minimal health risk,’ by the Dine Safe website [2].  These violations are more of a common occurrence, resulting in **36 % (32464 of 90827)** of all inspections during the period from July 2016 – June 2018. The five most common type of ‘minor’ violations are as follows:
  
*	‘Operator fail to properly wash surfaces in rooms’ with **9947 violations**.
*	‘Operator fail to properly wash equipment’ with **8118 violations**.
*	‘Operator fail to properly wash equipment’ with **6713 violations**.
*	‘Operator fail to properly maintain equipment (NON-FOOD)’ with **2666 violations**.
*	‘Operator fail to provide proper equipment’ with **2141 violations**. 

A health inspector can issue a ticket of compliance, and if this violation is repeated at the next inspection, a fine ranging from $45 to $370 may be issued [2]. 
	‘Significant’ violations are the next most common, resulting in **26% (23405 of 90827)** of all inspections. ‘Significant’ violations present a potential health hazard and must be corrected within the next 24-48 hours or legal action may be taken; these violations indirectly involve food, handling, preparation, and storage [2]. The five most common type of ‘Significant’ violations are as follows:
*	‘FAIL TO PROVIDE THERMOMETER IN STORAGE COMPARTMENT O. REG  562/90 SEC. 21’ with **1478 violations**.
*	‘FAIL TO HAVE TEST REAGENT AVAILABLE AT  PLACE OF SANITIZATION O. REG  562/90 SEC. 75(2)’ with **1381 violations**.
*	‘Operator fail to use proper procedure(s) to ensure food safety’ with **1347 violations**.
*	‘Operator fail to provide adequate pest control’ with **1106 violations**.
*	‘OPERATOR FAIL TO ENSURE COVER WILL PREVENT CONTAMINATION OR ADULTERATION O. REG  562/90 SEC. 59(C)(II)’ with **1070 violations**.

‘Crucial’ violations are the rarest resulting in **2% (2236 of 90827)** of all inspections. These violations present an immediate health hazard and directly involve food. Such violations must be corrected immediately or an ‘Order to close’ can be issued [2]. The five most common type of ‘Crucial’ violations are as follows:
*	‘Operator fail to ensure food is not contaminated/adulterated’ with **778 violations**.
*	‘Operator fail to maintain hazardous food(s) at 4C (40F) or colder’ with **674 violations**.
*	‘Operator fail to maintain hazardous foods at 60C (140F) or hotter’ with **211 violations**.
*	‘Employee fail to wash hands when required’ with **217 violations**.
*	‘Operator fail to wash hands when required’ with **90 violations**.

All the statistics above are obtained from the City of Toronto, open data catalogue [3]. This data source contains information regarding the violations, and data regarding the business name and location. However, this data does not contain valuable information regarding business practices and the overall sentiment of customers regarding an establishment. To obtain relevant information regarding the business’s practices, a yelp dataset (will be referred to as the Yelp DS in this document) was combined with the health inspections dataset (will be referred to as the DineSafe DS in this document). 

# Data Engineering/Auditing

## Auditing/Cleaning the DineSafe Data Set
The DineSafe DS contains information regarding 90827 health inspections from the time period between July 2016 through June 2018. The dataset contains the following data about the establishments:
* Establishment Name.
* Establishment Address.
* Establishment Status.
* Establishment Type, which contains 54 different establishment types ranging from ‘Restaurant’ to ‘Hospitals & Health Facilities’.
* Latitude.
* Longitude.

Additionally, the dataset contains the following data regarding the inspection:
* Inspection Date.
* Minimum number of inspections per year. This could be 1,2, or 3 depending on the type of establishment, and the type of food prepared [2].
* Severity, which includes the four classes mentioned in the Introduction section.
* Action, which is dependent upon the severity.
* Amount Fined, which is a consequence of the action.
* Court Outcome, which is again dependent upon the severity and action.

The dataset contains multiple inspections regarding a given establishment caused by repeat investigations, due to requirements of compliance from a previous investigation, added to the fact that some businesses require a minimum of 2 or 3 inspections per year. The goal of the predictive model is to forecast the outcome of a given inspection, assuming that it is a new investigation, without any previous knowledge. Therefore, the data used in the predictive model meets the following criteria:

* Each establishment has a record of only one inspection.
* The inspection record used will be the most recent.
* Repeat inspections resulting from previous violations are not included in the data.

The preceding criteria was met by cleaning the data using the following steps:

* The DineSafe DS was grouped by the three years (2016,2017 & 2018).
* The grouped datasets were sorted by date.
* The duplicates were removed using ‘Establishment ID’, which is a unique key for each establishment. The earliest records were kept, this would eliminate any repeat inspections resulting from previous violations.
* Once the duplicates have been removed, the three grouped data sets were merged.
* Duplicates were removed from the merged data set, keeping the most recent inspection. This was done to have more pertinent data in the data set. 

The removing of duplicates results in a total of 16160 establishment records.

## Merging the DineSafe DS with the Yelp DS

The Yelp DS contains important information regarding business practices, and the public sentiment about the business. The Yelp DS contains data regarding the business location, by way of the longitude and latitude. The two datasets were combined as follows:

* The longitude and latitude from both datasets were compared for matches.
* A tolerance level for the matching was set, which translate to 1 m in distance [3].
* As an additional measure, the establishment names in both datasets were first cleaned (by removing any spacing and using lower case letters), and then compared for matches on the first 5 letters.

Combining the two datasets resulted in reducing the data to 5639 records, which includes data regarding business practices of 5639 businesses, as well as the outcome of their most recent inspection.

## Cleaning Combined Dataset

The combined dataset contains data such as ‘Action’, ‘Amount Fined’, & ‘Court Outcome’, which are dependent upon the ‘Severity’ of a violation. The model aims to predict the ‘Severity’ of a violation. Including columns such as ‘Action’ and ‘Amount Fined’ would result in a data leak, therefore, these columns were removed from the dataset.
A great deal of the features regarding Business practices were attributes such as ‘Good for Kids’ or ‘Dogs Allowed’, which results in a binary outcome. The null values for these features were set to 0. Additional features which had categorical outcomes were assigned dummy variables.
Business opening and closing times could provide key insights into whether an inspection will result in a violation. The null values in opening and closing times for a given day were filled by the values of the opening and closing times for which data is available. To elaborate, if a business is open from Monday through Saturday, but closed on Sundays, the null values in Sunday were filled by the Monday times. If no values on opening and closing times were found, the mean time values were assigned to the null values.

# Statistical Analysis

## Spearman-R Test
To gain insight into the which features contributed to a violation a spearman r-test was conducted. The four classes for severity were assigned numerical values for increasing severity as follows:
* ‘Pass’ was assigned a value of 0.
* ‘Minor’ was assigned a value of 1.
* ‘Significant’ was assigned a value of 2.
* ‘Crucial’ was assigned a value of 3.

The Spearman’s correlation is a statistical measure of the strength of the monotonic relationship two sets of data. The interpretation of the statistics is similar to that of the Pearson correlation coefficient. The following results show the Spearman R-value for features, that had spearman r values greater than 0.1 and a p-value less than 0.05.

<p float = "center">
  <img src= "Figures/R_values_v5.png" width = 600 >
</p>

## Chi-Squared Tests – Establishment Type

The dataset contains information regarding the type of an establishment. The types can vary from ‘Bake shops’, ‘Butcher Shop’, to ‘Mobile Food Preparation Premises’, which includes a total of 42 different establishment types. 
With the goal of checking if certain business types were treated differently a chi-squared test was performed. The refined data set contains data about 5639 health inspections on 5639 businesses. From the 5639 inspections, 3211 resulted in a violation (‘Minor’, ‘Significant’, or ‘Crucial’) and 2428 resulted in a ‘Pass’. These were the expected values for which the comparison is made against. Grouped statistics were obtained for all the establishment types, summing up the violation and pass count. The results of the chi-squared test are shown below, for establishment types that had p-values less than 0.05.  The Infraction ratio is the ratio of the sum of infractions by the total number of inspections.

<p float = "center">
  <img src= "Figures/Establishment_Type_Chi.png" width = 600 >
</p>

## Chi-Squared Tests – Neighborhood

A similar analysis was done to check for differences between the outcomes of an inspection when the neighborhood of a business was taken into consideration. Grouped statistics were obtained for 72 distinct neighborhoods. Similar to the previous analysis, of the 5639 inspections 3211 resulted in violations and 2428 resulted in a ‘Pass’. The results of the Chi-Squared test are shown below for neighborhoods with p-values less than 0.05. As before, the Infraction ratio is the ratio of the sum of infractions by the total number of inspections.
The neighborhoods shaded in green have a more positive bias, this is may be due to certain socio-economic factors that are not present in the data. The neighborhoods shaded in red have a more negative bias. It is also likely that some of these neighborhoods have a higher concentration of restaurants, which from the previous analysis was shown to have a more negative bias than the average.

<p float = "center">
  <img src= "Figures/Neighborhood_Chi.png" width = 600 >
</p>

# Model Optimization and Results

As previously mentioned, there are two predictive models built, one to predict if a violation (of any type) will occur at a given inspection, and another model to predict the type of violation from the four classes, “Pass”, “Minor”, “Significant”, and “Crucial.

### Random Forest - Optimization

Random Forest models parallelly and independently fit decision tress fitting an individual tree to a random subset of data points. The model performance of Random forests increases with additional estimators reaching a point of diminishing returns. The random forest will be an average over all the trees(estimators), as the individual cases of overfitting are not common, they will disappear on average. A grid search was done to establish the best parameters for the Random Forest model, with the following details about the grid search:

* The training data was optimized on the number of trees, and the warm start condition. 
* A 5-fold cross-validation was performed.
* The performance metric was accuracy.

The results of the hyper-parameter optimization are shown below, with the best parameters being a model with 700 trees, set to a condition of false for the warm start. The highest cross-validation score was 0.671.

<p float = "center">
  <img src= "Figures/RF_Binary_optimization.png" width = 600 >
</p>

### Random Forests – Model Evaluation

The ROC curve and Confusion Matrix for the best Random Forest model evaluated on the unseen test data, along with the area under the ROC curve, F1 score, Precision and Recall are shown below.
	
<p float = "left">
  <img src="Figures/RF_Binary_Conf_Mat.png" width = 450  >
  <img src="Figures/RF_ROC_AUC.png" width = 350 >
</p>

As observed in the confusion matrix, the model does a reasonable job of predicting passes and infractions. However, it has a considerable number of false positives, misclassifying passes as infractions. 

### XG Boost - Optimization

In addition to the Random Forest model, a Boosting method was considered by optimizing an XGBoost model. Boosting methods work by fitting a sequence of models, each of which is trained to focus on predictions the previous model got wrong, accomplished by re-weighting each data point so that the misclassified data contributes more to the error. Gradient Boosting fits each sub-model to the residuals of the previous models. With increasing number of estimators boosting methods can tend to overfit. A grid search was done to establish the best parameters for the XGBoost model, with the following details about the grid search:
* The training data was optimized on the number of estimators, and the learning rate. 
* A 5-fold cross-validation was performed.
* The performance metric was accuracy.

The results of the hyper-parameter optimization are shown below, with the best parameters being a model with 950 estimators, with a learning rate of 0.03, achieving a highest cross-validation score of 0.673.

<p float = "center">
  <img src= "Figures/XG_Boos_Binary_Opt.png" width = 600 >
</p>

### XGBoost – Model Evaluation

The model with the best parameters was evaluated on the unseen testing data. The ROC curve and confusion matrix, along with the area under the ROC curve, F1 score, Precision and Recall are shown below.

<p float = "left">
  <img src="Figures/XG_Boost_Binary_Conf_Matr.png" width = 400 >
  <img src="Figures/XG_Boost_Binary_ROC.png" width = 400 >
</p>

Interestingly, this model performs better than the best Random Forest model, with 44 less false positives and 11 less false negatives. 

	



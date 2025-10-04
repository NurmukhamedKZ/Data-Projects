### It's my pet projects as ML engineer


- Projects with using Linear regression:
    1. House_rent_project
    


## Some statistics from the House rent predictor:
####  **Before removing outliers**
 
- **MSE**: 1847277896.97
- **RMSE**: 42979.97
- **MAE**: 21208.08
- **R2 Score**: 0.5365
- **Adjusted R2**: 0.5223949221615469 
- Cross-validation scores: [ 0.55129507 0.19055452 0.26400282 0.24365718 -0.94940058] 
- Average CV score: 0.0600 (+/- 1.0403)

---
#### **After removing outliers**

- **MSE**: 44584129.51
- **RMSE**: 6677.13
- **MAE**: 4772.53
- **R2 Score**: 0.6840
- **Adjusted R2**: 0.6717423761871585
- Cross-validation scores: [0.67977215 0.66872775 0.47602472 0.57717581 0.42115716]
- Average CV score: 0.5646 (+/- 0.2053)
---
#### **After turning month into string**

- **MSE**: 44319032.79
- **RMSE**: 6657.25
- **MAE**: 4741.99
- **R2 Score**: 0.6859
- **Adjusted R2**: 0.6727865265935423 
- Cross-validation scores: [0.68144882 0.67007972 0.47966192 0.57718857 0.41892005] 
- Average CV score: 0.5655 (+/- 0.2066)

---
#### **After making polynomial regression for "Size" feature**

Polynomial regression Metrics: 
- **MSE**: 43019580.62
- **RMSE**: 6558.93
- **MAE**: 4671.06
- **R2 Score**: 0.6951
- **Adjusted R2**: 0.6819381925928998
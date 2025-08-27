graph LR
  %% Topologia de anel (bidirecional)
  PC1[PC1]
  PC2[PC2]
  PC3[PC3]
  PC4[PC4]
  PC5[PC5]
  
  PC1 --- PC2
  PC2 --- PC3
  PC3 --- PC4
  PC4 --- PC5
  PC5 --- PC1

  style PC1 fill:#FFD700,stroke:#333,stroke-width:2px
  style PC2 fill:#FF6347,stroke:#333,stroke-width:2px
  style PC3 fill:#90EE90,stroke:#333,stroke-width:2px
  style PC4 fill:#1E90FF,stroke:#333,stroke-width:2px
  style PC5 fill:#DA70D6,stroke:#333,stroke-width:2px

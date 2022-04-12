AG_complexity <- function(x) {
 L <- length(x)
 if ( sum (x) == L || sum(x) ==0) { 
   Complexity <- 0
  } else {
 M <- matrix(0, L, L)
 for(i in 1:(L - 1)) {
  M[i, 2] <- ifelse(x[i] != x[i + 1], 1, 0)
 }
 for (j in 3:L) {
   for (i in 1:(L - j + 1)) {
     for (k in 2:(j - 1)) {
       r <- j + i - k
       if (M[i, k] != M[r, k]) {
       M[i, j] <- 1
       }
     }
   }
 }
 
 Profile <- apply(M[, 2:L], 2, sum)        
 a <- 2:L
 weights <- 1 / (L - a + 1)
 Complexity <- sum(Profile * weights)
 }
 return(Complexity)
 }
Array_complexity <- function(y) {
 Diagonals_1 <- split(y, col(y) - row(y))  
 Diagonals_2 <- split(y, row(y)+ col(y))
 Diagonals_list <- c(Diagonals_1,Diagonals_2)
 R <- sum(apply (y, 1, AG_complexity))
 C <- sum(apply( y, 2, AG_complexity))
 D <- sum(sapply(Diagonals_list, function(z) if (length(z) == 1) {0} else if (length(z) == 2) ifelse( sum(z) == 1, 1, 0) else AG_complexity(z)))
 m <- dim(y)[1]
 n <- dim(y)[2]
 d <- m + n -1
 S <- R / m + C / n + D / d
 X <- d - 1 +2 * (m - 1) * (n - 1) / d
 L <- 4 * m * n / (3 * d + 1) 
 U <- (L - 1) * (S / X)
 return(U) 
}



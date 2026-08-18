# Standalone Dockerfile for Transaction Ledger Service (Java 26 / Spring Boot 4)
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

RUN apk add --no-cache curl bash unzip

COPY pom.xml mvnw ./
COPY .mvn ./.mvn

RUN chmod +x mvnw && ./mvnw dependency:go-offline -B || true

COPY src ./src
RUN ./mvnw clean package -DskipTests

# Stage de Produção
FROM eclipse-temurin:21-jre-alpine AS runner

WORKDIR /app

RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-XX:+UseZGC", "-XX:+ZGenerational", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]

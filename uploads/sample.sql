-- Create database schema
CREATE DATABASE [StudentConsulting]
GO

USE [StudentConsulting]
GO

-- Create tables
CREATE TABLE [dbo].[Users] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [Username] NVARCHAR(50) NOT NULL,
    [Password] NVARCHAR(255) NOT NULL,
    [Email] NVARCHAR(100) NOT NULL,
    [FullName] NVARCHAR(100),
    [PhoneNumber] VARCHAR(15),
    [Avatar] NVARCHAR(MAX),
    [IsActive] BIT DEFAULT 1,
    [CreatedAt] DATETIME2 DEFAULT GETDATE(),
    [UpdatedAt] DATETIME2,
    [LastLoginAt] DATETIME2
)
GO

CREATE TABLE [dbo].[Departments] (
    [Id] INT IDENTITY(1,1) PRIMARY KEY,
    [Name] NVARCHAR(100) NOT NULL,
    [Description] NTEXT,
    [IsActive] BIT DEFAULT 1,
    [CreatedAt] DATETIME2 DEFAULT GETDATE()
)
GO

CREATE TABLE [dbo].[Questions] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    [Title] NVARCHAR(255) NOT NULL,
    [Content] NVARCHAR(MAX),
    [UserId] UNIQUEIDENTIFIER,
    [DepartmentId] INT,
    [Status] INT DEFAULT 0,
    [ViewCount] INT DEFAULT 0,
    [CreatedAt] DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY ([UserId]) REFERENCES [Users]([Id]),
    FOREIGN KEY ([DepartmentId]) REFERENCES [Departments]([Id])
)
GO

-- Insert sample data
INSERT INTO [dbo].[Users] WITH (NOLOCK)
    ([Username], [Password], [Email], [FullName])
VALUES
    ('admin', CONVERT(NVARCHAR(255), 'hashedpassword123'), 'admin@example.com', N'Administrator'),
    ('user1', CONVERT(NVARCHAR(255), 'userpass123'), 'user1@example.com', N'User One')
GO

-- Sample stored procedure
CREATE PROCEDURE [dbo].[GetUserQuestions]
    @UserId UNIQUEIDENTIFIER,
    @StartDate DATETIME2,
    @EndDate DATETIME2
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP 100
        q.[Id],
        q.[Title],
        q.[Content],
        u.[FullName] AS UserName,
        d.[Name] AS DepartmentName,
        ISNULL(q.[ViewCount], 0) AS Views,
        DATEDIFF(DAY, q.[CreatedAt], GETDATE()) AS DaysAgo,
        CASE 
            WHEN q.[Status] = 0 THEN 'Pending'
            WHEN q.[Status] = 1 THEN 'Answered'
            ELSE 'Closed'
        END AS StatusText
    FROM [dbo].[Questions] q WITH (NOLOCK)
    INNER JOIN [dbo].[Users] u WITH (NOLOCK) ON q.[UserId] = u.[Id]
    LEFT JOIN [dbo].[Departments] d WITH (NOLOCK) ON q.[DepartmentId] = d.[Id]
    WHERE q.[UserId] = @UserId
    AND q.[CreatedAt] BETWEEN @StartDate AND DATEADD(DAY, 1, @EndDate)
    ORDER BY q.[CreatedAt] DESC
END
GO

-- Sample complex query
SELECT 
    u.[FullName],
    d.[Name] AS Department,
    COUNT(q.[Id]) AS QuestionCount,
    MAX(q.[CreatedAt]) AS LastQuestionDate,
    CONVERT(MONEY, AVG(CAST(q.[ViewCount] AS FLOAT))) AS AvgViews
FROM [dbo].[Users] u WITH (NOLOCK)
INNER JOIN [dbo].[Questions] q WITH (NOLOCK) ON u.[Id] = q.[UserId]
INNER JOIN [dbo].[Departments] d WITH (NOLOCK) ON q.[DepartmentId] = d.[Id]
WHERE u.[IsActive] = 1
AND LEN(u.[Username]) > 3
AND q.[CreatedAt] >= DATEADD(MONTH, -1, GETDATE())
GROUP BY u.[FullName], d.[Name]
HAVING COUNT(q.[Id]) > 0
ORDER BY QuestionCount DESC 
package Managers;

import Classes.Client;

import java.math.BigInteger;
import java.sql.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

public class ClientManager implements ManagerDB{
    private Client client;
    private Connection con;

    public ClientManager(Connection con, Client client) throws SQLException{
        // Create a variable for the connection string.
        //String connectionUrl = "jdbc:sqlserver://DESKTOP-0M0S9AF;databaseName=NFBankDB;integratedSecurity=true;";
        //Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        this.con = con;
        this.client = client;
        /*String SQL = "SELECT * FROM account_status";
        Statement stmt = con.createStatement();
        ResultSet rs = stmt.executeQuery(SQL);

        // Iterate through the data in the result set and display it.
        while (rs.next()) {
            System.out.println(rs.getString(1) + " " + rs.getString(2));
        }*/
    }

    public void create() throws SQLException{
        String createSQL = "INSERT INTO client (id, username, password, birth_date, [name], surname) VALUES " +
                "(?, ?, ?, ?, ?, ?);";
        PreparedStatement psstmt = con.prepareStatement(createSQL);
        psstmt.setString(1, client.getIdClient().toString());
        psstmt.setString(2, client.getUsername());
        psstmt.setString(3, client.getPassword());
        if (client.getBirthOfDate() != null) {
            String dt = client.getBirthOfDate().toString();
            psstmt.setString(4, dt);
        }
        else{
            psstmt.setNull(4, Types.DATE);
        }
        psstmt.setString(5, client.getFirstName());
        psstmt.setString(6, client.getLastName());
        psstmt.executeUpdate();
    }

    public void delete() throws SQLException{
        String deleteSql = "DELETE FROM client where id = ?";
        PreparedStatement prepStmt = con.prepareStatement(deleteSql);
        prepStmt.setString(1, client.getIdClient().toString());
        prepStmt.executeUpdate();
    }

    public void update(String upd, String name) throws SQLException {
        String updSql = "UPDATE client " +
                "SET " + upd + " = ? where id = ?";
        PreparedStatement stmt = con.prepareStatement(updSql);
        if (name != null){
            stmt.setString(1, name);
        }
        else{
            stmt.setNull(1, Types.TIMESTAMP);
        }
        stmt.setString(2, client.getIdClient().toString());
        stmt.executeUpdate();
    }

    public List<Client> select() throws SQLException, ParseException {
        String selectSql = "SELECT * FROM client where id = ?";
        PreparedStatement stmt = con.prepareStatement(selectSql);
        stmt.setString(1, client.getIdClient().toString());
        ResultSet rs = stmt.executeQuery();
        List<Client> result = new ArrayList<Client>();
        while (rs.next()) {
            Date bdate = null;
            if (rs.getString("birth_date") != null){
                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
                bdate = new java.sql.Date(dateFormat.parse(rs.getString("birth_date")).getTime());
            }
            Client cl = new Client(new BigInteger(rs.getString("id")), rs.getString("username"),
                    rs.getString("password"), bdate, rs.getString("name"),
                    rs.getString("surname"));
            result.add(cl);
        }
        return result;
    }
}

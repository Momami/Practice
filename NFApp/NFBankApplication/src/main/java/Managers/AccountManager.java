package Managers;

import Classes.Account;

import java.math.BigInteger;
import java.sql.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

public class AccountManager implements ManagerDB{
    private Account account;
    private Connection con;

    public AccountManager(Connection con, Account account){
        this.account = account;
        this.con = con;
    }

    public void create() throws SQLException {
        String createSQL;

            createSQL = "INSERT INTO account (id, balance, open_date, close_date, status, id_client) VALUES " +
                    "(?, ?, ?, ?, ?, ?);";

        PreparedStatement psstmt = con.prepareStatement(createSQL);
        psstmt.setString(1, account.getIdAccount().toString());
        psstmt.setString(2, Float.toString(account.getBalance()));
        psstmt.setString(3, account.getOpen_date().toString());
        if (account.getClose_date() != null)
            psstmt.setString(4, account.getClose_date().toString());
        else
            psstmt.setNull(4, Types.DATE);
        psstmt.setString(5, account.getStatus().getId());
        psstmt.setString(6, "26531872653815");
        psstmt.executeUpdate();
    }

    public void delete() throws SQLException{
        String deleteSql = "DELETE FROM account where id = ?";
        PreparedStatement prepStmt = con.prepareStatement(deleteSql);
        prepStmt.setString(1, account.getIdAccount().toString());
        prepStmt.executeUpdate();
    }

    public void update(String upd, String name) throws SQLException {
        String updSql = "UPDATE account " +
                            "SET " + upd + " = ? where id = ?";
        PreparedStatement stmt = con.prepareStatement(updSql);
        if (name != null){
            stmt.setString(1, name);
        }
        else{
            stmt.setNull(1, Types.TIMESTAMP);
        }
        stmt.setString(2, account.getIdAccount().toString());
        stmt.executeUpdate();
    }

    public List<Account> select() throws SQLException, ParseException {
        String selectSql = "SELECT * FROM account where id = ?";
        PreparedStatement prepstmt = con.prepareStatement(selectSql);
        prepstmt.setString(1, account.getIdAccount().toString());
        ResultSet rs = prepstmt.executeQuery();
        List<Account> result = new ArrayList<Account>();
        while (rs.next()) {
            BigInteger id = new BigInteger(rs.getString("id"));
            float balance = Float.parseFloat(rs.getString("balance"));
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
            Date open = new java.sql.Date(dateFormat.parse(rs.getString("open_date")).getTime());
            Date close = null;
            if (rs.getString("close_date") != null)
                close = new java.sql.Date(dateFormat.parse(rs.getString("close_date")).getTime());
            ResultSet stat = (con.prepareStatement("SELECT name FROM account_status WHERE name = " +
                    rs.getString("status"))).executeQuery();
            Account.AccountStatus status = Account.AccountStatus.getStatus(Integer.parseInt
                    (rs.getString("status")));
            Account account = new Account(id, balance, open, close, status);
            result.add(account);
        }
        return result;
    }
}

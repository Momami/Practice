package Classes;

import java.math.BigInteger;
import java.sql.Date;



public class Account {

    public enum AccountStatus{
        OPEN(1),
        CLOSED(2),
        SUSPEND(3);
        String num;

        AccountStatus(int num){
            this.num = Integer.toString(num);
        }

        public String getId(){
            return num;
        }

        public static AccountStatus getStatus(int id){
            return id == 1 ? OPEN : id == 2 ? CLOSED : SUSPEND;
        }
    }

    private BigInteger idAccount;
    private float balance;
    private Date open_date;
    private Date close_date;
    private AccountStatus status;

    public Account(BigInteger idAccount, float balance, Date open_date, Date close_date, AccountStatus status) {
        this.idAccount = idAccount;
        this.balance = balance;
        this.open_date = open_date;
        this.close_date = close_date;
        this.status = status;
    }

    public BigInteger getIdAccount() {
        return idAccount;
    }

    public void setIdAccount(BigInteger idAccount) {
        this.idAccount = idAccount;
    }

    public float getBalance() {
        return balance;
    }

    public void setBalance(float balance) {
        this.balance = balance;
    }

    public Date getOpen_date() {
        return open_date;
    }

    public void setOpen_date(Date open_date) {
        this.open_date = open_date;
    }

    public Date getClose_date() {
        return close_date;
    }

    public void setClose_date(Date close_date) {
        this.close_date = close_date;
    }

    public AccountStatus getStatus() {
        return status;
    }

    public void setStatus(AccountStatus status) {
        this.status = status;
    }
}

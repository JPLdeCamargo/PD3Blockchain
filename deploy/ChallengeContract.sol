// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

contract ChallengeContract {
    struct PostDetails {
        string text;
        string media_link;
    }

    struct Bet {
        address bet_owner;
        uint256 amount;
        bool in_favor;
    }

    struct Vote {
        address voter;
        bool is_valid;
    }

    struct Post {
        uint256 post_id;
        address poster_adress;
        PostDetails post_details;
        mapping(uint256 => Bet) bets;
        uint256 n_bets;
        uint256 end_date;
        PostDetails validity_media;
        bool votes_enabled;
        mapping(uint256 => Vote) votes;
        uint256 n_votes;
    }

    mapping(uint256 => Post) posts;
    uint256 current_id = 0;

    function addPost(
        string memory text,
        string memory media,
        uint256 date
    ) public returns(uint256) {
        Post storage post = posts[current_id];
        post.post_id = current_id;
        post.poster_adress = msg.sender;
        post.post_details = PostDetails(text, media);
        post.n_bets = 0;
        post.end_date = date;
        post.validity_media = PostDetails("", "");
        post.votes_enabled = false;
        post.n_votes = 0;
        current_id++;
        return post.post_id;
    }

    function addBet(uint256 post_id, bool in_favor) public payable {
        uint256 temp_index = posts[post_id].n_bets;
        posts[post_id].bets[temp_index] = Bet(msg.sender, msg.value, in_favor);
        posts[post_id].n_bets++;
    }

    function addValidityMedia(
        uint256 post_id,
        string memory text,
        string memory link
    ) public returns (string memory) {
        if (bytes(text).length == 0 && bytes(link).length == 0)
            return "ERROR, no validity information has been specified";
        if (msg.sender != posts[post_id].poster_adress)
            return "ERROR, FUNCTION MUST BE CALLED BY POST OWNER ONLY";
        posts[post_id].validity_media = PostDetails(text, link);
        return "Validity media has been added";
    }

    function enableVotes(uint256 post_id) public {
        posts[post_id].votes_enabled = true;
    }

    function vote(uint256 post_id, bool is_valid) public {
        require(posts[post_id].votes_enabled);
        bool alreadyVoted = false;
        for (uint256 i = 0; i < posts[post_id].n_votes; i++) {
            if (posts[post_id].votes[i].voter == msg.sender) {
                alreadyVoted = true;
                break;
            }
        }
        require(!alreadyVoted);
        uint256 temp_index = posts[post_id].n_votes;
        posts[post_id].votes[temp_index] = Vote(msg.sender, is_valid);
        posts[post_id].n_votes++;
    }

    // verifica se é um apostador
    function isBetter(uint256 post_id, address voter)
        private
        view
        returns (bool)
    {
        for (uint256 i = 0; i < posts[post_id].n_bets; i++) {
            if (voter == posts[post_id].bets[i].bet_owner) {
                return true;
            }
        }
        return false;
    }

    // checar se a media é valida, caso seja dinheiro vai para quem apostou a favor
    // caso contrario vai para aqueles que apostaram contra
    function checkValidity(uint256 post_id) private view returns (bool) {
        Post storage p = posts[post_id];
        uint256 vote_score = 0;
        uint256 max_vote_score = 0;
        for (uint256 i = 0; i < p.n_votes; i++) {
            uint256 score = 1;
            if (isBetter(post_id, p.votes[i].voter)) score = score * 5;
            max_vote_score += score;
            score = p.votes[i].is_valid == true ? score : 0;
            vote_score += score;
        }
        if ((vote_score * 100) / (max_vote_score * 100) > 50) return true;
        return false;
    }

    // distribuir dinheiro entre ganhadores
    function distributeBets(bool is_valid, uint256 post_id) private {
        Post storage p = posts[post_id];
        address[] memory receivers;
        uint256 total_value = 0;
        for (uint256 i = 0; i < p.n_bets; i++) {
            total_value += p.bets[i].amount;
            if (p.bets[i].in_favor == is_valid)
                receivers[receivers.length] = p.bets[i].bet_owner;
        }
        uint256 money_per_winner = total_value / receivers.length;
        for (uint256 i = 0; i < receivers.length; i++) {
            payable(receivers[i]).transfer(money_per_winner);
        }
    }

    function terminate(uint256 post_id) public {
        if (block.timestamp < posts[post_id].end_date) return;
        distributeBets(checkValidity(post_id), post_id);
    }

    function getPost(uint256 post_id)
        public
        view
        returns (
            string memory,
            string memory,
            uint256,
            uint256,
            uint256,
            string memory,
            string memory
        )
    {
        Post storage post = posts[post_id];
        return (
            post.post_details.text,
            post.post_details.media_link,
            post.end_date,
            post.n_bets,
            post.n_votes,
            post.validity_media.text,
            post.validity_media.media_link
        );
    }
}
